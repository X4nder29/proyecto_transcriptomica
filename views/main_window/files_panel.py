from asyncio import constants
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QScrollArea,
    QMenu
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from .file_widget import FileWidget


class FilesPanel(QWidget):

    def __init__(self, settings, add_file_path, file_widget_click):
        super().__init__()

        self.settings = settings
        self.add_file_path = add_file_path
        self.file_widget_click = file_widget_click

        self.setupUi()

    def setupUi(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(0)

        # Header

        header = QWidget(self)
        header_layout = QHBoxLayout(header)

        header.setObjectName("header")
        header.setStyleSheet(
            """
            QWidget#header {
                border-bottom: 2px solid #353535;
            }
            """
        )

        self.search_icon = QLabel(header)
        self.search_icon.setPixmap(
            QPixmap("assets/search.svg").scaled(
                32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        self.search_icon.setFixedSize(32, 32)
        self.search_icon.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.search_input = QLineEdit(header)
        self.search_input.setPlaceholderText("Buscar archivo")
        self.search_input.setStyleSheet(
            """
            QLineEdit {
                background: transparent;
                border: none;
                padding: 5px;
                font-size: 14px;
                color: white;
            }
        """
        )
        self.search_input.clearFocus()

        self.upload_button = QPushButton("Subir", header)
        self.upload_button.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
            }"""
        )
        self.upload_button.clicked.connect(self.openFileDialog)

        header_layout.addWidget(self.search_icon)
        header_layout.addWidget(self.search_input)
        header_layout.addWidget(self.upload_button)

        # Body

        content = QScrollArea(self)
        content.setWidgetResizable(True)
        content.setStyleSheet(
            """
            QScrollArea {
                background: none;
                border: none;
            }
            """
        )

        file_list = QWidget()
        list_layout = QVBoxLayout(file_list)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(0)

        file_paths = self.settings.value("file_paths", [], type=list)

        for i in range(16):
            btn = FileWidget(f"Archivo {i}")

            

            list_layout.addWidget(btn)

        content.setWidget(file_list)

        layout.addWidget(header)
        layout.addWidget(content)
        """ layout.addWidget(file_list, 1) """

    def openFileDialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "Fastq (*.fastq)",
        )

        if file_path:
            print(f"Archivo seleccionado: {file_path}")
            self.add_file_path(file_path)
            self.check_files_paths()
        else:
            print("No se seleccionó ningún archivo")
            QMessageBox.warning(self, "Error", "No se seleccionó ningún archivo")

    def fileWidgetClicked(self):
        file_paths = self.settings.value("file_paths", [], type=list)
        print(file_paths)
        file_paths.clear()
        self.settings.setValue("file_paths", file_paths)
        self.file_widget_click()