from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)
from .widgets.side_bar import SideBar
from .widgets.content import Content

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("MainWindow")
        self.setWindowTitle("TranscriptoHub")
        self.setGeometry(500, 250, 1000, 600)

        self.setupUi()

    def setupUi(self):

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.side_bar = SideBar(self)
        self.content = Content(self)

        self.side_bar.home_button.clicked.connect(
            lambda: self.changePanel(0, self.side_bar.home_button)
        )
        self.side_bar.bioinformatics_button.clicked.connect(
            lambda: self.changePanel(1, self.side_bar.bioinformatics_button)
        )
        self.side_bar.graphics_button.clicked.connect(
            lambda: self.changePanel(2, self.side_bar.graphics_button)
        )
        self.side_bar.settings_button.clicked.connect(
            lambda: self.changePanel(3, self.side_bar.settings_button)
        )

        self.main_layout.addWidget(self.side_bar)
        self.main_layout.addWidget(self.content, 1)

    def changePanel(self, index, button):
        if index != self.content.main_layout.currentIndex():
            self.content.main_layout.setCurrentIndex(index)
            self.side_bar.changeButtonsStyle(index)
