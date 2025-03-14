from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QPushButton, QFileDialog, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt


class EmptyFilePanel(QWidget):

    def __init__(self, add_file_path):
        super().__init__()

        self.add_file_path = add_file_path

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("Welcome to TranscriptoHub")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        indication_label = QLabel("Open existing files from disk")
        indication_label.setStyleSheet("font-size: 16px; color: #AAA;")

        spacer = QSpacerItem(20, 50)

        button = QPushButton()
        button.setIcon(QIcon("assets/add.svg"))
        button.setIconSize(button.sizeHint())
        button.setFixedSize(60, 60)
        button.clicked.connect(self.open_file_dialog)

        button_name = QLabel("Upload Files")
        button_name.setStyleSheet("font-size: 14px;")

        layout.addWidget(title_label, alignment=Qt.AlignHCenter)
        layout.addWidget(indication_label, alignment=Qt.AlignHCenter)
        layout.addItem(spacer)
        layout.addWidget(button, alignment=Qt.AlignHCenter)
        layout.addWidget(button_name, alignment=Qt.AlignHCenter)

    def open_file_dialog(self):
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
