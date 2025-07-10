from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from .kraken_panel_head import KrakenPanelHead
from .kraken_panel_body import KrakenPanelBody


class KrakenPanel(QWidget):
    """
    KrakenPanel is a QWidget that represents the Kraken panel in the main window.
    It is used to display and manage Kraken-related functionalities.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("KrakenPanel")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.main_layout)

        self.head = KrakenPanelHead(self)
        self.main_layout.addWidget(self.head)

        self.body = KrakenPanelBody(self)
        self.main_layout.addWidget(self.body)
