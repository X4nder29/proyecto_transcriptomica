from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QLabel,
    QFileDialog,
    QLineEdit
)
from PySide6.QtCore import Qt
from ....widgets.line_edit_with_button import LineEditWithButton


class PeFilesArea(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("FilesArea")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setup_ui()

    def setup_ui(self):

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)

        self.input_file_1_label = QLabel("Archivo de Entrada 1", self)
        self.input_file_1_label.setObjectName("FilesLabel")
        self.input_file_1_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.input_file_1_pe = LineEditWithButton("assets/file.svg")
        self.input_file_1_pe.button.clicked.connect(
            lambda: self.open_file_dialog(self.input_file_1_pe.line_edit)
        )

        self.input_file_2_label = QLabel("Archivo de Entrada 2", self)
        self.input_file_2_label.setObjectName("FilesLabel")
        self.input_file_2_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.input_file_2_pe = LineEditWithButton("assets/file.svg")
        self.input_file_2_pe.button.clicked.connect(
            lambda: self.open_file_dialog(self.input_file_2_pe.line_edit)
        )

        self.output_file_1_label = QLabel("Archivo de Salida 1", self)
        self.output_file_1_label.setObjectName("FilesLabel")
        self.output_file_1_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.output_file_1_pe = LineEditWithButton("assets/file.svg")

        self.output_file_2_label = QLabel("Archivo de Salida 2", self)
        self.output_file_2_label.setObjectName("FilesLabel")
        self.output_file_2_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.output_file_2_pe = LineEditWithButton("assets/file.svg")
        self.output_file_2_pe.button.clicked.connect(lambda: print("hello, boy"))

        self.main_layout.addWidget(self.input_file_1_label)
        self.main_layout.addWidget(self.input_file_1_pe)
        self.main_layout.addWidget(self.input_file_2_label)
        self.main_layout.addWidget(self.input_file_2_pe)
        self.main_layout.addWidget(self.output_file_1_label)
        self.main_layout.addWidget(self.output_file_1_pe)
        self.main_layout.addWidget(self.output_file_2_label)
        self.main_layout.addWidget(self.output_file_2_pe)

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
