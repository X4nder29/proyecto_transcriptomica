from os import startfile
from shutil import rmtree
from typing import Callable, Optional
from pathlib import Path
from PySide6.QtWidgets import QProgressDialog, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from views.widgets import DatabaseItemWidget, DatabaseManagerDialog
from utils import (
    clear_layout,
    strip_any_suffix,
)
from workers import DownloadWorker, UngzipWorker, UntarWorker, FilenameWorker


class DatabaseManagerController:

    _workers: list[DownloadWorker | UngzipWorker | UntarWorker] = []

    def __init__(
        self,
        view: DatabaseManagerDialog,
        available_db: Callable[[], list[dict[str, str]]],
        downloaded_db: Callable[[], list[Path]],
        db_folder: Path,
        add_database: Callable[[str, str], None],
        remove_database_by_link: Callable[[str], None],
    ):
        self.view = view
        self.available_db = available_db
        self.downloaded_db = downloaded_db
        self.db_folder = db_folder
        self.add_database = add_database
        self.remove_database_by_link = remove_database_by_link

        self._load_databases()
        self.view.add_button.clicked.connect(self.download_new_database)

    def download_new_database(self):
        """
        Opens a dialog to download a new database.
        The dialog allows the user to select a database from a list of available databases.
        """
        link = self.view.link_line_edit.text()

        if not link:
            QMessageBox.warning(
                self.view,
                "Error",
                "Please enter a valid database link.",
            )
            return

        self._save_database(link)
        self._download_database(link)
        self.view.link_line_edit.clear()

    def _show_download_progress(self, name: str):
        self.progress = QProgressDialog(
            f"Downloading database{f" :{name}" if name else ""}",
            "Cancel",
            0,
            100,
            self.view,
        )
        self.progress.setWindowTitle("Downloading Database")
        self.progress.setMinimumDuration(0)
        self.progress.setValue(0)
        self.progress.setAutoClose(True)
        self.progress.setAutoReset(True)
        self.progress.setCancelButton(QPushButton("Cancel", self.progress))
        self.progress.setMinimumWidth(400)
        self.progress.setMinimumHeight(100)
        self.progress.setWindowModality(Qt.WindowModality.NonModal)
        self.progress.show()

    def _load_databases(self):

        available_db = self.available_db()
        downloaded_db = self.downloaded_db()

        installed_databases: list[Path] = []
        uninstalled_databases: list[dict[str, str]] = []

        installed_databases.extend(downloaded_db)
        uninstalled_databases.extend(available_db)
        uninstalled_databases = list(
            filter(
                lambda x: strip_any_suffix(x["name"])
                not in list(map(lambda y: y.stem, installed_databases)),
                uninstalled_databases,
            )
        )

        print("Installed databases:", installed_databases)
        print("Uninstalled databases:", uninstalled_databases)

        # Clear existing items in the layouts

        clear_layout(self.view.installed_layout)
        clear_layout(self.view.uninstalled_layout)

        # Add installed databases

        self.view.installed_scroll_area.setVisible(bool(installed_databases))

        for installed_database in installed_databases:
            installed_item = DatabaseItemWidget(
                installed_database.name,
                str(installed_database),
                parent=self.view.uninstalled_widget,
                installed=True,
            )
            installed_item.open_action.clicked.connect(
                lambda _, f=installed_database.parent.as_posix(): (startfile(f))
            )
            installed_item.delete_action.clicked.connect(
                lambda _, f=installed_database: self._delete_database_from_disk_dialog(
                    f
                )
            )
            self.view.installed_layout.addWidget(installed_item)

        # Add uninstalled databases

        self.view.uninstalled_scroll_area.setVisible(bool(uninstalled_databases))

        for uninstalled_database in uninstalled_databases:
            uninstalled_item = DatabaseItemWidget(
                uninstalled_database["name"],
                uninstalled_database["link"],
                parent=self.view.uninstalled_widget,
            )
            uninstalled_item.install_action.clicked.connect(
                lambda _, n=uninstalled_database["name"], l=uninstalled_database[
                    "link"
                ]: self._download_database(l, n)
            )
            uninstalled_item.delete_action.clicked.connect(
                lambda _, l=uninstalled_database[
                    "link"
                ]: self._delete_database_from_settings_dialog(l)
            )
            self.view.uninstalled_layout.addWidget(uninstalled_item)

    # delete database

    def _delete_database_from_disk_dialog(self, path: Path):
        """
        Opens a dialog to confirm the deletion of a database from disk.
        If confirmed, it deletes the database from disk and settings.
        """
        if not path:
            return

        reply = QMessageBox.question(
            self.view,
            "Confirmar eliminación",
            "¿Está seguro de que desea eliminar esta base de datos del disco?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self._delete_database_from_disk(path)

    def _delete_database_from_disk(self, path: Path):
        if not path.exists():
            return

        if path.is_file():
            path.unlink(missing_ok=True)

        if path.is_dir():
            rmtree(path)

        self._load_databases()

    def _delete_database_from_settings_dialog(self, link: str):
        """
        Opens a dialog to confirm the deletion of a database from settings.
        If confirmed, it deletes the database from settings.
        """
        if not link:
            return

        reply = QMessageBox.question(
            self.view,
            "Confirmar eliminación",
            "¿Está seguro de que desea eliminar esta base de datos de la configuración?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self._delete_database_from_settings(link)

    def _delete_database_from_settings(self, link: str):
        if not link:
            return

        self.remove_database_by_link(link)
        self._load_databases()

    # save database

    def _save_database(self, link: str):
        worker = FilenameWorker(link, parent=self.view)

        worker.finished.connect(
            lambda name, l=link: self._on_filename_finished(name, l)
        )
        worker.error.connect(self._on_filename_error)

        self._workers.append(worker)
        worker.start()

    def _on_filename_finished(self, name: str, link: str):
        """
        Callback for when the filename is obtained from the worker.
        It adds the database to the settings.
        """
        self.add_database(name, link)

    def _on_filename_error(self, error: str):
        """
        Callback for when an error occurs in the worker.
        It displays an error message to the user.
        """
        print(f"Error obtaining filename: {error}")

    # download database

    def _download_database(self, link: str, name: Optional[str] = None):
        self._show_download_progress(name)

        worker = DownloadWorker(link, self.db_folder.as_posix(), parent=self.view)

        worker.progress_changed.connect(self.progress.setValue)
        worker.file_name_signal.connect(self.on_download_file_name)
        worker.finished_signal.connect(
            lambda path, w=worker: self._on_download_finished(Path(path), w)
        )
        worker.error.connect(lambda error: print(Path(__file__).name, "error:", error))

        self.progress.canceled.connect(
            lambda: (
                worker.terminate(),
                self.progress.deleteLater(),
            )
        )

        self._workers.append(worker)
        worker.start()

    def on_download_file_name(self, name: str):
        self.progress.setLabelText(f"Downloading database: {name}")

    def _on_download_finished(self, path: Path, worker: DownloadWorker):
        self.progress.setLabelText("Database downloaded")
        self._workers.remove(worker)
        self.check_suffix(path)

    # ungzip

    def _ungzip_database(self, file: Path):
        """
        Unzips a gzip file and emits progress signals.
        If the file is successfully unzipped, it checks the suffix of the file.
        """
        print(Path(__file__).name, "-", "ungzip database:", file)

        worker = UngzipWorker(file)

        worker.progress.connect(self.progress.setValue)
        worker.finished.connect(
            lambda path, src=file, w=worker: self._on_ungzip_finished(src, path, w)
        )
        worker.error.connect(
            lambda error: print(Path(__file__).name, "error:", error),
        )

        self.progress.setLabelText("Ungzipping database...")
        self._workers.append(worker)
        worker.start()

    def _on_ungzip_finished(self, src: Path, path: Path, worker: UngzipWorker):
        """
        Callback for when the ungzip worker finishes.
        It checks the suffix of the file to determine the next action.
        """
        src.unlink(missing_ok=True)
        self.progress.setLabelText("Gzip extraction completed")
        self._workers.remove(worker)
        self.check_suffix(path)

    # untar

    def _untar_database(self, file: Path):
        worker = UntarWorker(file, file.parent)

        worker.progress_changed.connect(self.progress.setValue)
        worker.finished.connect(
            lambda path, src=file, w=worker: self._on_untar_finished(src, path, w)
        )
        worker.error.connect(
            lambda error: print(Path(__file__).name, "error:", error),
        )

        self.progress.setLabelText("Untarring database...")
        self._workers.append(worker)
        worker.start()

    def _on_untar_finished(self, src: Path, path: Path, worker: UntarWorker):
        """
        Callback for when the untar worker finishes.
        It checks the suffix of the file to determine the next action.
        """
        src.unlink(missing_ok=True)
        self.progress.setLabelText("Tar extraction completed")
        self._workers.remove(worker)
        self.check_suffix(path)

    # check suffix

    def check_suffix(self, file: Path):
        """
        Checks the suffix of the file name and returns the appropriate suffix.
        """
        print(Path(__file__).name, "-", "check suffix:", file.suffix)

        if file.is_file() and file.suffix == ".tar":
            print(Path(__file__).name, "-", "untar database")
            self._untar_database(file)
            return

        if file.is_file() and file.suffix == ".gz":
            print(Path(__file__).name, "-", "ungzip database")
            self._ungzip_database(file)
            return

        if file.is_file() and file.suffix:
            QMessageBox.warning(
                self.view,
                "Error",
                f"Unsupported file type: {file.suffix}. Please use .tar or .gz files.",
            )
            print(Path(__file__).name, "-", "unsupported file type:", file.suffix)

        print(Path(__file__).name, "-", "no suffix found, deleting file")
        self._load_databases()
        self.progress.close(),
