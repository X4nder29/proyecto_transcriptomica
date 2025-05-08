from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QMessageBox,
)
from PySide6.QtCore import Qt


class FastqcPanelHead(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("FastqcPanelHead")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setupUi()

    def setupUi(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        # head widgets setup can be added here

        self.setLayout(self.main_layout)