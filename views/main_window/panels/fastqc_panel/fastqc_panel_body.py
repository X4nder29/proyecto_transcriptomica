from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from pathlib import Path
from .widgets import Section1, Section2, Section3


class FastqcPanelBody(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("FastqcPanelBody")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_style_sheet()
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

    def load_style_sheet(self):
        styles_path = Path(__file__).parent / "fastqc_panel_body.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())
