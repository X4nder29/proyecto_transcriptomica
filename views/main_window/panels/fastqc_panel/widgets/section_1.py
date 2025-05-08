from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QStyle,
    QStyleOption,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from pathlib import Path
from .file_list import FileList
from .basic_statistics import BasicStatistics


class Section1(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("Section1")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_style_sheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        self.file_list = FileList(self)
        self.basic_statistics = BasicStatistics(self)

        # body widgets setup can be added here

        self.main_layout.addWidget(self.file_list, alignment=Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.basic_statistics, alignment=Qt.AlignmentFlag.AlignBottom)
        self.setLayout(self.main_layout)

    def load_style_sheet(self):
        styles_path = Path(__file__).parent / "section_1.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
