from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout
)
from PySide6.QtGui import QIcon
from .home_window_body import HomeWindowBody


class HomeWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("HomeWindow")
        self.setWindowTitle("TranscriptoHub")
        self.setWindowIcon(QIcon(":/assets/icon.svg"))
        self.setMinimumSize(1000, 600)
        self.setAcceptDrops(True)

        # central widget

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)

        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)

        # body

        self.body = HomeWindowBody(self)
        self.body.setObjectName("Body")
        self.central_layout.addWidget(self.body)
