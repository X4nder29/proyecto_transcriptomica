from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QStackedWidget,
    QVBoxLayout,
    QStyle,
    QStyleOption,
    QSizePolicy,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import QFile, QTextStream, Signal
from .upload_files_push_button import UploadFilesPushButton
from .workspace_files_page import WorkspaceFilesPage


class WorkspaceFilesWidget(QWidget):
    dropped = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("FilesArea")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAcceptDrops(True)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        self.stacked = QStackedWidget(self)
        self.stacked.setObjectName("FilesAreaStacked")
        self.main_layout.addWidget(self.stacked)

        self.upload_files_push_button = UploadFilesPushButton(self)
        self.stacked.addWidget(self.upload_files_push_button)

        self.file_list_widget = WorkspaceFilesPage(self)
        self.stacked.addWidget(self.file_list_widget)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
        super().paintEvent(event)

    def dragEnterEvent(self, event):
        # Aceptamos solo si vienen URLs (ficheros)
        mime = event.mimeData()
        if mime.hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        return super().dragLeaveEvent(event)

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        # Extraemos las rutas de los archivos y las mostramos
        paths = [url.toLocalFile() for url in urls]
        self.setText("Archivos soltados:\n" + "\n".join(paths))
        event.acceptProposedAction()
