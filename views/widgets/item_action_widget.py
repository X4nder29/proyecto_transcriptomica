from pathlib import Path
from PySide6.QtWidgets import (
    QStyle,
    QStyleOption,
    QPushButton,
)
from PySide6.QtGui import QIcon, QPainter
from PySide6.QtCore import QFile, QTextStream


class ItemActionWidget(QPushButton):
    def __init__(self, icon_path: str, parent=None):
        super().__init__(parent)
        self.icon_path = icon_path
        self.setup_ui()
        self.load_stylesheet()

    def setup_ui(self):
        self.setObjectName("ItemActionWidget")
        self.setIcon(QIcon(self.icon_path))

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
