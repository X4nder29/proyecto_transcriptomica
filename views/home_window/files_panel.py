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
    QMenu,
    QSizePolicy
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from .file_widget import FileWidget
from views.main_window import MainWindow


class FilesPanel(QWidget):

    def __init__(self, settings, add_file_path, file_widget_click):
        super().__init__()

        self.settings = settings
        self.add_file_path = add_file_path
        self.file_widget_click = file_widget_click

        self.setupUi()

    def setupUi(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 0, 28, 0)
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
                28, 28, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation
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
                background: red;
                border: none;
            }
            """
        )

        file_list = QWidget()

        list_layout = QVBoxLayout(file_list)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(0)

        file_paths = self.settings.value("file_paths", [], type=list)

        for file_path in file_paths:
            btn = FileWidget(file_path)
            btn.clicked.connect(self.fileWidgetClicked)
            list_layout.addWidget(btn)

        list_layout.addStretch()

        content.setWidget(file_list)

        layout.addWidget(header)
        layout.addWidget(content)

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
        else:
            print("No se seleccionó ningún archivo")
            QMessageBox.warning(self, "Error", "No se seleccionó ningún archivo")

    def fileWidgetClicked(self):
        print("File widget clicked")
        self.window().close()
        MainWindow().show()
