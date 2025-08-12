from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QHBoxLayout,
)
from PySide6.QtGui import QGuiApplication, QIcon, QColor
from PySide6.QtCore import Qt
from .main_window_sidebar import MainWindowSideBar
from .main_window_content import MainWindowContent
from utils import tint_icon


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi()

        QGuiApplication.styleHints().colorSchemeChanged.connect(self.update_icon)
        QGuiApplication.styleHints().colorSchemeChanged.emit(
            QGuiApplication.styleHints().colorScheme()
        )

    def setupUi(self):

        self.setObjectName("MainWindow")
        self.setWindowTitle("TranscriptoHub")
        self.setGeometry(250, 200, 1300, 700)

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.central_widget.setLayout(self.main_layout)

        self.side_bar = MainWindowSideBar(self)
        self.content = MainWindowContent(self)

        self.side_bar.button_group.idClicked.connect(lambda id: self.changePanel(id))

        self.main_layout.addWidget(self.side_bar)
        self.main_layout.addWidget(self.content, 1)

    def changePanel(self, index):
        if index != self.content.main_layout.currentIndex():
            self.content.main_layout.setCurrentIndex(index)

    def update_icon(self, scheme: Qt.ColorScheme):
        self.icon = (
            QIcon(":/assets/icon.svg")
            if scheme == Qt.ColorScheme.Dark
            else tint_icon(":/assets/icon.svg", QColor("#006a66"))
        )
        self.setWindowIcon(self.icon)
