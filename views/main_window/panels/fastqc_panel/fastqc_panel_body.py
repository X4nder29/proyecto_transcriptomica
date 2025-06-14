from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QFile, QTextStream
from pathlib import Path
from .widgets import Section1, Section2, Section3


class FastqcPanelBody(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("FastqcPanelBody")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        self.section1 = Section1(self)
        self.section2 = Section2(self)
        self.section3 = Section3(self)

        self.main_layout.addWidget(self.section1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.section2, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.section3)


        # body widgets setup can be added here

        self.setLayout(self.main_layout)

        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
