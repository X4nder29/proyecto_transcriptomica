from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QStackedLayout,
    QMessageBox
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSettings
from .empty_file_panel import EmptyFilePanel
from .files_panel import FilesPanel


class HomeWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("TranscriptoHub")
        self.setFixedSize(800, 500)
        self.setAcceptDrops(True)

        self.settings = QSettings("preferences.ini", QSettings.IniFormat)
        print(self.settings.fileName())

        self.setupUi()

    def setupUi(self):

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.main_layout = QStackedLayout(central_widget)

        empty_file_panel = EmptyFilePanel(
            add_file_path=self.addFilePath
        )
        self.main_layout.addWidget(empty_file_panel)

        files_panel = FilesPanel(
            settings=self.settings,
            add_file_path=self.addFilePath,
            file_widget_click=self.checkFilesPaths,
        )
        self.main_layout.addWidget(files_panel)

        self.checkFilesPaths()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            print(url.toLocalFile())
            if url.toLocalFile().endswith(".fastq"):
                self.addFilePath(url.toLocalFile())
            else:
                print("Invalid file type")
                QMessageBox.warning(self, "Error", "Tipo de archivo inválido")

    def addFilePath(self, path):
        files_pahts = self.settings.value("file_paths", [], type=list)
        files_pahts.append(path)
        self.settings.setValue("file_paths", files_pahts)

        self.checkFilesPaths()

    def removeFilePath(self, path):
        files_pahts = self.settings.value("file_paths", [], type=list)
        files_pahts.remove(path)
        self.settings.setValue("file_paths", files_pahts)

        self.checkFilesPaths()

    def checkFilesPaths(self):
        file_paths = self.settings.value("file_paths", [], type=list)

        if file_paths:
            self.main_layout.setCurrentIndex(1)
        else:
            self.main_layout.setCurrentIndex(0)
