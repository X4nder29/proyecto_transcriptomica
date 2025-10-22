import os
import shutil
from pathlib import Path
from typing import Optional
from PySide6.QtWidgets import QFileDialog, QProgressDialog
from PySide6.QtCore import Qt, QTimer, QThread, QObject, Slot
from utils import (
    get_current_workspace,
    get_current_workspace_source_folder_path,
    get_trimmed_files_paths,
    get_sorted_files_paths,
    get_source_files_paths,
    get_krakened_files_paths,
    get_fastqc_output_folder_path_by_file,
)
from views.main_window.panels.home_panel import HomePanel
from views.main_window.panels.home_panel.widgets import WorkspaceFileItemWidget
from workers import MoveFileWorker, FileScannerWorker


class HomePanelController:

    def __init__(self, view: HomePanel):

        self.view = view

        self._scan_ui_handler = FileScanUIHandler(self)

        QTimer.singleShot(0, lambda: self.load_workspace_files())

        self.view.header.user_manual_button.clicked.connect(self.open_user_manual)

        self.view.content.files_area.upload_files_push_button.clicked.connect(
            self.open_file_dialog
        )
        self.view.content.files_area.file_list_widget.upload_button.clicked.connect(
            self.open_file_dialog
        )
        self.view.content.files_area.upload_files_push_button.dropped.connect(
            lambda file: self.drop_file(file)
        )

        # filter buttons

        self.view.content.files_area.file_list_widget.all_button.clicked.connect(
            lambda: self.load_workspace_files()
        )
        self.view.content.files_area.file_list_widget.trimmed_button.clicked.connect(
            lambda: self.load_workspace_files("Recortados")
        )
        self.view.content.files_area.file_list_widget.krakened_button.clicked.connect(
            lambda: self.load_workspace_files("Taxonomizado")
        )
        self.view.content.files_area.file_list_widget.sorted_button.clicked.connect(
            lambda: self.load_workspace_files("Ordenados")
        )

        #

        current_workspace = get_current_workspace()

        if current_workspace is None:
            self.view.content.current_workspace.set_workspace_name("Error Workspace")
            self.view.content.current_workspace.set_workspace_path(
                "/error/in/workspace"
            )
        else:
            self.view.content.current_workspace.set_workspace_name(
                current_workspace.name
            )
            self.view.content.current_workspace.set_workspace_path(
                current_workspace.as_posix()
            )

    def open_user_manual(self):
        """
        Open the user manual in a new support window.
        """
        from views.support_window import SupportWindow

        self.support_window = SupportWindow(self.view.window())
        self.support_window.setWindowFlag(Qt.WindowType.Window)
        self.support_window.show()

    def open_file_dialog(self):
        file_filter = "RNA Files (*.fasta *.fa *.fastq *.fq *.gff *.gtf *.sam *.bam)"
        file_path, _ = QFileDialog.getOpenFileName(
            self.view, "Select an RNA file", "", file_filter
        )

        if not file_path:
            print(__name__, "-", "No file selected.")
            return

        file_path = Path(file_path)

        if not file_path.exists():
            print(__name__, "-", f"File {file_path} does not exist.")
            return

        print(__name__, "-", f"File selected: {file_path}")

        self.upload_file(file_path)

    def drop_file(self, file: str):
        """
        Handle file drop event.
        """
        print(__name__, "-", "File dropped:", file)

        if not file:
            print(__name__, "-", "No file path provided.")
            return

        file_path = Path(file.replace("file:///", ""))

        if not file_path.exists():
            print(__name__, "-", f"File {file_path} does not exist.")
            return

        if not file_path.is_file():
            print(__name__, "-", f"Path {file_path} is not a file.")
            return

        if not file_path.suffix in {".fasta", ".fa", ".fastq", ".fq"}:
            print(__name__, "-", f"File {file_path} is not a supported RNA file type.")
            return

        print(__name__, "-", f"File dropped: {file_path}")

        self.upload_file(file_path)

    def upload_file(self, file_path: Path):
        dialog = QProgressDialog("Moviendo archivo...", None, 0, 0, self.view)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.setMinimumDuration(0)
        dialog.setCancelButton(None)
        dialog.setWindowTitle("Procesando")
        dialog.show()

        self.thread = MoveFileWorker(
            str(file_path), str(get_current_workspace_source_folder_path())
        )
        self.thread.finished.connect(lambda _, __, d=dialog: self._on_upload_file_finished(d))
        self.thread.start()

    def _on_upload_file_finished(self, dialog: QProgressDialog):
        dialog.close()
        self.load_workspace_files()

    def load_workspace_files(self, fltr: Optional[str] = None):

        self._scanner_thread = QThread()
        self._scanner_worker = FileScannerWorker(fltr)
        self._scanner_worker.moveToThread(self._scanner_thread)

        self._scanner_worker.finished.connect(
            self._scan_ui_handler.handle_scan_finished
        )
        self._scanner_worker.error.connect(self._scan_ui_handler.handle_scan_error)

        self._scanner_thread.started.connect(self._scanner_worker.run)
        self._scanner_worker.finished.connect(self._scanner_thread.quit)
        self._scanner_worker.finished.connect(self._scanner_worker.deleteLater)
        self._scanner_thread.finished.connect(self._scanner_thread.deleteLater)

        # arrancar
        self._scanner_thread.start()

    def _on_scan_error(self, msg: str):
        print("Error scanning files:", msg)
        if hasattr(self, "_loading_dialog"):
            self._loading_dialog.close()

    def _on_scan_finished(self, files_str_list):

        # limpiar elementos antiguos (hazlo en hilo UI)
        layout = self.view.content.files_area.file_list_widget.list_widget.scroll_content_layout
        # eliminar todos los widgets de forma segura
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        # si no hay archivos, mostrar la página vacía
        if not files_str_list:
            self.current_files = []
            print("No files found")
            return

        # crear widgets (UI thread) a partir de la lista de rutas
        for fpath in files_str_list:
            p = Path(fpath)
            if not p.exists():
                continue
            file_list_item = WorkspaceFileItemWidget(
                p.name,
                str(p),
                parent=self.view.content.files_area.file_list_widget,
            )
            # abrir carpeta padre (capturamos p como valor por defecto)
            file_list_item.open_action.clicked.connect(
                lambda _, p=p: os.startfile(p.parent.as_posix())
            )
            file_list_item.delete_action.clicked.connect(
                lambda _, p=p: self.show_delete_source_file_dialog(p)
            )
            layout.addWidget(file_list_item)

        self.view.content.files_area.stacked.setCurrentIndex(1)
        self.current_files = [Path(p) for p in files_str_list]

    def show_delete_source_file_dialog(self, source_file: Path):
        """
        Show a confirmation dialog before deleting a source file.
        """
        from PySide6.QtWidgets import QMessageBox

        reply = QMessageBox.question(
            self.view,
            "Delete Source File",
            f"Are you sure you want to delete {source_file.name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.delete_file(source_file)

    def delete_file(self, file: Path):
        """
        Delete the source file from the workspace.
        """
        if not file.exists():
            return

        try:
            fastqc_output_folder = get_fastqc_output_folder_path_by_file(file)
            print(fastqc_output_folder)

            if fastqc_output_folder is not None:
                shutil.rmtree(fastqc_output_folder)

            file.unlink(True)

            self.load_workspace_files()
        except Exception as e:
            print(f"Error deleting file {file}: {e}")

    def open_user_manual(self):
        from views.support_window.support_window import SupportWindow
        from controllers.support_window_controller import SupportWindowController

        self.support_window = SupportWindow(self.view.window())
        self.support_window_controller = SupportWindowController(
            self.support_window, "Inicio"
        )
        self.support_window.show()


class FileScanUIHandler(QObject):
    """Handler que vive en hilo UI; sus slots actualizan la UI de forma segura."""

    def __init__(self, controller):
        super().__init__()  # sin parent o parent=self.view si lo prefieres
        self.controller = controller

    @Slot(list)
    def handle_scan_finished(self, files_str_list):
        # Este método se ejecuta en el hilo del FileScanUIHandler (UI thread).
        self.controller._on_scan_finished(files_str_list)

    @Slot(str)
    def handle_scan_error(self, msg):
        self.controller._on_scan_error(msg)
