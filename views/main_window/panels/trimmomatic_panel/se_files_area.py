from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from ....widgets.line_edit_with_button import LineEditWithButton


class SeFilesArea(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("FilesArea")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setup_ui()

    def setup_ui(self):

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)

        self.input_file_label = QLabel("Archivo de Entrada", self)
        self.input_file_label.setObjectName("FilesLabel")
        self.input_file_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.input_file_se = LineEditWithButton(":/assets/file.svg")
        self.input_file_se.setObjectName("FilesInput")
        self.input_file_se.button.clicked.connect(
            lambda: self.open_file_dialog(self.input_file_se.line_edit)
        )

        self.output_file_label = QLabel("Archivo de Salida", self)
        self.output_file_label.setObjectName("FilesLabel")

        self.output_file_se = LineEditWithButton(":/assets/file.svg")
        self.output_file_se.setObjectName("FilesInput")

        self.main_layout.addWidget(self.input_file_label)
        self.main_layout.addWidget(self.input_file_se)
        self.main_layout.addWidget(self.output_file_label)
        self.main_layout.addWidget(self.output_file_se)
        self.main_layout.addStretch()

    def open_file_dialog(self, line_edit):
        filter = (
            "Archivos FASTA/FASTQ (*.fasta *.fa *.fastq *.fq)"
        )

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo FASTA o FASTQ", "", filter
        )

        if file:
            line_edit.setText(file)