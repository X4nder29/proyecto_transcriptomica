from pathlib import Path
from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QHBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import QFile, QTextStream


class LineEditWithButton(QWidget):

    def __init__(self, icon_path: str, parent=None):
        super().__init__(parent=parent)

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
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
