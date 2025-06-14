from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QLabel,
)
from PySide6.QtCore import QFile, QTextStream
from pathlib import Path


class PanelHeadSimple(QWidget):

    def __init__(self, title, parent=None):
        super().__init__(parent)

        self.title = title

        self.setObjectName("PanelHead")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        self.title = QLabel(self.title, self)
        self.title.setObjectName("title")
        self.main_layout.addWidget(self.title)

        # head widgets setup can be added here

        self.setLayout(self.main_layout)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
