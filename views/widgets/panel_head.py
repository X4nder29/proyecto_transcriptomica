from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtGui import QIcon


class PanelHead(QWidget):

    def __init__(self, title, parent=None):
        super().__init__(parent=parent)

        self.title = title

        self.setObjectName("PanelHead")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_style_sheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)
        self.setLayout(self.main_layout)

        # title label

        self.title = QLabel(self.title, self)
        self.title.setObjectName("title")
        self.main_layout.addWidget(self.title)

        # add stretch

        self.main_layout.addStretch()

        # play button

        self.play_button = QPushButton(self)
        self.play_button.setObjectName("action_button")

        self.play_button_icon = QIcon(":/assets/play.svg")
        self.play_button.setIcon(self.play_button_icon)

        self.main_layout.addWidget(self.play_button)

        # star button

        self.star_button = QPushButton(self)
        self.star_button.setObjectName("action_button")

        self.star_button_icon = QIcon(":/assets/outlined_star.svg")
        self.star_button.setIcon(self.star_button_icon)

        self.main_layout.addWidget(self.star_button)

    def load_style_sheet(self):
        styles_path = Path(__file__).with_suffix(".qss")
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())
