from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QMessageBox,
)
from PySide6.QtCore import Qt
from .trimmomatic_panel_head import TrimmomaticPanelHead
from .trimmomatic_panel_body import TrimmomaticPanelBody


class TrimmomaticPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("TrimmomaticPanel")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setupUi()

    def setupUi(self):

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # head

        self.head = TrimmomaticPanelHead(self)

        # body

        self.body = TrimmomaticPanelBody(self)

        # add widgets

        self.main_layout.addWidget(self.head, alignment=Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.body)

    def show_error_dialog(self, message):
        QMessageBox.critical(
            self,
            "Error",
            message,
            QMessageBox.StandardButton.Ok,
        )
