from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QMessageBox,
)
from PySide6.QtCore import Qt
from ....widgets import PanelHead
from .fastqc_panel_body import FastqcPanelBody


class FastqcPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("FastqcPanel")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setupUi()

    def setupUi(self):

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # head

        self.head = PanelHead("FastQC", self)

        # body

        self.body = FastqcPanelBody(self)

        # add widgets

        self.main_layout.addWidget(self.head, alignment=Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.body)
        self.setLayout(self.main_layout)



    def show_error_dialog(self, message):
        QMessageBox.critical(
            self,
            "Error",
            message,
            QMessageBox.StandardButton.Ok,
        )