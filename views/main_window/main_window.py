from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)
from PySide6.QtGui import QIcon
from .main_window_sidebar import MainWindowSideBar
from .main_window_content import MainWindowContent

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("MainWindow")
        self.setWindowTitle("TranscriptoHub")
        self.setGeometry(250, 200, 1000, 700)
        self.setWindowIcon(QIcon(":/assets/icon.svg"))

        self.setupUi()

    def setupUi(self):

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.side_bar = MainWindowSideBar(self)
        self.content = MainWindowContent(self)

        self.side_bar.button_group.idClicked.connect(lambda id: self.changePanel(id))

        self.main_layout.addWidget(self.side_bar)
        self.main_layout.addWidget(self.content, 1)

    def changePanel(self, index):
        if index != self.content.main_layout.currentIndex():
            self.content.main_layout.setCurrentIndex(index)
