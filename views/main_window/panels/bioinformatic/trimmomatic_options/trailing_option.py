from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QLabel,
    QStyleOption,
    QStyle,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from .number_selector import NumberSelector


class TrailingOption(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("TrailingOption")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.setupUi()

    def setupUi(self):

        self.setMinimumWidth(150)
        self.setMinimumHeight(50)
        self.setStyleSheet(
            """
            QWidget#TrailingOption {
                background-color: #404040;
                border-radius: 10px;
            }
            """
        )

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # head

        self.title = QLabel("Trailing", self)
        self.title.setObjectName("title")
        self.title.setStyleSheet(
            """
            QLabel#title {
                font-size: 14px;
                font-weight: bold;
                color: white;
            }
            """
        )

        # value

        self.value_number_selector = NumberSelector(self)

        #

        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.value_number_selector)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
