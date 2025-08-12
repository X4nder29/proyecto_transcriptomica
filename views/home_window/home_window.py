from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PySide6.QtGui import QIcon, QColor, QGuiApplication
from PySide6.QtCore import Qt
from .home_window_body import HomeWindowBody
from utils import tint_icon


class HomeWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.update_icon)
        self.update_icon(QGuiApplication.styleHints().colorScheme())
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("HomeWindow")
        self.setWindowTitle("TranscriptoHub")
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

    def update_icon(self, scheme: Qt.ColorScheme):
        self.icon = (
            QIcon(":/assets/icon.svg")
            if scheme == Qt.ColorScheme.Dark
            else tint_icon(":/assets/icon.svg", QColor("#006a66"))
        )
        self.setWindowIcon(self.icon)
