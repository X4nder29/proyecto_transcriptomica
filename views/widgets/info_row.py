from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSizePolicy,
    QLabel,
    QStyle,
    QStyleOption,
)
from PySide6.QtCore import Qt, QFile, QTextStream
from PySide6.QtGui import QPainter
from pathlib import Path


class InfoRow(QWidget):
    def __init__(self, title, value, parent=None):
        super().__init__(parent)

        self.title = title
        self.value = value

        self.setObjectName("InfoRow")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_stylesheet()
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

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
