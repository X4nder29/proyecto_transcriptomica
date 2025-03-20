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


class LeadingOption(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("LeadingOption")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.setupUi()

    def setupUi(self):

        self.setMinimumWidth(150)
        self.setMinimumHeight(50)
        self.setStyleSheet(
            """
            QWidget#LeadingOption {
                background-color: #404040;
                border-radius: 10px;
            }
            """
        )

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # head

        self.title = QLabel("Leading", self)
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

        self.value_number_selector = NumberSelector(self)

        #

        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.value_number_selector)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
