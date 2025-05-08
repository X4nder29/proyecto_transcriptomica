from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)
from PySide6.QtCore import Qt
from .programs_area import ProgramsArea


class HomePanelBody(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("HomePanelBody")

        self.load_stylesheet()

        self.setupUi()

    def setupUi(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.programs_area = ProgramsArea(self)
        self.main_layout.addWidget(self.programs_area, alignment=Qt.AlignmentFlag.AlignRight)

    def load_stylesheet(self):
        styles_path = Path(__file__).parent / "home_panel_body.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())