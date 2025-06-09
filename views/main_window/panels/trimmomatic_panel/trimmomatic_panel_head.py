from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSizePolicy,
    QLabel,
    QPushButton,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt


class TrimmomaticPanelHead(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("TrimmomaticPanelHead")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.loadStylesheet()

        self.setupUi()

    def setupUi(self):

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        self.title = QLabel("Trimmomatic", self)
        self.title.setObjectName("title")

        self.play_button = QPushButton(self)
        self.play_button.setObjectName("action_button")

        self.play_button_icon = QIcon("assets/play.svg")
        self.play_button.setIcon(self.play_button_icon)

        # star button

        self.star_button = QPushButton(self)
        self.star_button.setObjectName("action_button")

        self.star_button_icon = QIcon("assets/outlined_star.svg")
        self.star_button.setIcon(self.star_button_icon)

        # add widgets

        self.main_layout.addWidget(self.title)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.play_button)
        self.main_layout.addWidget(self.star_button)

    def loadStylesheet(self):
        styles_path = Path(__file__).parent / "trimmomatic_panel_head.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())
