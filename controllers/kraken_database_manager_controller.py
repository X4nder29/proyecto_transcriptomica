import os
import shutil
from pathlib import Path
from PySide6.QtWidgets import QProgressDialog, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from views.widgets import (
    DatabaseManagerDialog,
    DatabaseItemWidget,
)
from utils import (
    split_name,
    get_kraken2_databases,
    add_kraken2_database,
    remove_kraken2_database_by_link,
    get_kraken2_database_folders,
    get_kraken2_database_folder_from_settings,
    get_kraken2_databases_folder_path,
)
from workers import DownloadWorker, UntarWorker


class KrakenDatabaseManagerController:
    """
    Controller for managing the database in the Kraken panel.
    This controller handles the logic for installing, uninstalling,
    and updating databases, as well as managing the UI interactions.
    """

    _name_threads = []
    _download_threads = []

    def __init__(self, view: DatabaseManagerDialog):
        self.view = view
        self._load_databases()

    # load databases

    def _check_installed_databases(self):
        pass

    def _load_databases(self):
        databases = get_kraken2_databases()
        databases_folders = get_kraken2_database_folders()

        folder_stems = {folder.stem: folder for folder in databases_folders}

        installed_databases = []
        uninstalled_databases = []

        for database in databases:
            key = split_name(database["name"])
            folder = folder_stems.get(key)

            if folder is not None:
                installed_databases.append({**database, "folder": folder.as_posix()})
            else:
                uninstalled_databases.append(database)

        # Clear existing items in the layouts

        for i in range(self.view.installed_layout.count()):
            item = self.view.installed_layout.itemAt(i).widget()
            if item:
                item.deleteLater()

        for i in range(self.view.uninstalled_layout.count()):
            item = self.view.uninstalled_layout.itemAt(i).widget()
            if item:
                item.deleteLater()

        # Update installed and uninstalled databases sections

        if installed_databases:
            self.view.installed_scroll_area.setVisible(True)

            for installed_database in installed_databases:
                installed_item = DatabaseItemWidget(
                    installed_database["name"],
                    installed_database["link"],
                    parent=self.view.uninstalled_widget,
                    installed=True,
                )
                installed_item.open_action.clicked.connect(
                    lambda _, f=installed_database["folder"]: (os.startfile(f))
                )
                installed_item.delete_action.clicked.connect(
                    lambda _, f=installed_database[
                        "folder"
                    ]: self._delete_database_from_disk_dialog(Path(f))
                )
                self.view.installed_layout.addWidget(installed_item)
        else:
            self.view.installed_scroll_area.setVisible(False)

        if uninstalled_databases:
            self.view.uninstalled_scroll_area.setVisible(True)

            for uninstalled_database in uninstalled_databases:
                uninstalled_item = DatabaseItemWidget(
                    uninstalled_database["name"],
                    uninstalled_database["link"],
                    parent=self.view.uninstalled_widget,
                )
                uninstalled_item.install_action.clicked.connect(
                    lambda _, n=uninstalled_database["name"], l=uninstalled_database[
                        "link"
                    ]: self._download_database(n, l)
                )
                uninstalled_item.delete_action.clicked.connect(
                    lambda _, l=uninstalled_database[
                        "link"
                    ]: self._delete_database_from_settings_dialog(l)
                )
                self.view.uninstalled_layout.addWidget(uninstalled_item)
        else:
            self.view.uninstalled_scroll_area.setVisible(False)

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
        if not path:
            return

        shutil.rmtree(path)
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

        remove_kraken2_database_by_link(link)
        self._load_databases()

    # dowload database

    def _download_database(self, name: str, link: str):

        # Check if the link is valid

        if not link:
            return

        # Progress dialog

        self.progress = QProgressDialog(
            f"Downloading database: {name}", "Cancel", 0, 100, self.view
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

        # Get destination folder

        dest = get_kraken2_database_folder_from_settings()

        if not dest:
            dest = get_kraken2_databases_folder_path()

        # file path

        input_file_path = dest / name
        output_folder_path = input_file_path.parent / input_file_path.stem

        # workers
        download_worker = DownloadWorker(link, dest, parent=self.view)

        untar_worker = UntarWorker(
            input_file_path,
            output_folder_path,
            parent=self.view,
        )

        # connect signals

        download_worker.progress_changed.connect(self.progress.setValue)
        download_worker.file_name_signal.connect(self.on_file_name)
        download_worker.finished_signal.connect(
            lambda _, __, th=download_worker: (
                self._download_threads.remove(th),
                untar_worker.start(),
                self.progress.setLabelText("Database downloaded, extracting..."),
            )
        )
        download_worker.start()
        self._download_threads.append(download_worker)

        untar_worker.progress_changed.connect(self.progress.setValue)
        untar_worker.finished.connect(
            lambda: (
                self.progress.setValue(100),
                self.progress.setLabelText(
                    "Database downloaded and extracted successfully."
                ),
                self._load_databases(),
                self.progress.deleteLater(),
                input_file_path.unlink(missing_ok=True),
            )
        )

        self.progress.canceled.connect(
            lambda: (
                download_worker.terminate(),
                untar_worker.terminate(),
                self.progress.deleteLater(),
            )
        )

    def on_file_name(self, name: str):
        self.progress.setLabelText(f"Downloading database: {name}")

    def on_download_finished(self, success: bool, info: str):
        if success:
            QMessageBox.information(
                self, "Descarga completada", f"El archivo se ha guardado en:\n{info}"
            )
        else:
            QMessageBox.critical(
                self, "Error al descargar", f"Ocurrió un error:\n{info}"
            )
