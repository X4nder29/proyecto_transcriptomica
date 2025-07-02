from pathlib import Path
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QFile, QTextStream


class ActionButtonWidget(QPushButton):
    def __init__(self, icon_path: str, tooltip: str, parent=None):
        super().__init__(parent=parent)
        self.icon_path = icon_path
        self.tooltip = tooltip
        self.setup_ui()
        self.load_stylesheet()

    def setup_ui(self):
        self.setObjectName("ActionButtonWidget")
        self.setToolTip(self.tooltip)
        self.setIcon(QIcon(self.icon_path))

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
