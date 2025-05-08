from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)


class HomePanelHead(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("HomePanelHead")

        self.load_stylesheet()

        self.setupUi()

    def setupUi(self):

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.panel_title = QLabel("TranscriptoHub", self)
        self.panel_title.setObjectName("PanelTitle")
        self.main_layout.addWidget(self.panel_title)

    def load_stylesheet(self):
        styles_path = Path(__file__).parent / "home_panel_head.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())
