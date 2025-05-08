from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSizePolicy,
    QLabel,
    QStyle,
    QStyleOption,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from pathlib import Path


class InfoRow(QWidget):
    def __init__(self, title, value, parent=None):
        super().__init__(parent)

        self.title = title
        self.value = value

        self.setObjectName("InfoRow")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_style_sheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        self.title = QLabel(self.title, self)
        self.title.setObjectName("InfoRowTitle")

        self.value = QLabel(self.value, self)
        self.value.setObjectName("InfoRowValue")

        # body widgets setup can be added here

        self.main_layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.value, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(self.main_layout)

    def load_style_sheet(self):
        styles_path = Path(__file__).parent / "info_row.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
