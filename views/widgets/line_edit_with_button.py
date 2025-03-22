from pathlib import Path
from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QHBoxLayout
from PySide6.QtGui import QIcon


class LineEditWithButton(QWidget):

    def __init__(self, icon_path: str):
        super().__init__()

        self.icon_path = icon_path

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):
        self.line_edit = QLineEdit()

        self.button = QPushButton()
        self.button.setIcon(QIcon(self.icon_path))

        layout = QHBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)

    def load_stylesheet(self):
        styles_path = Path(__file__).parent / "line_edit_with_button.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())
