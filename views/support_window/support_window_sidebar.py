from pathlib import Path
from PySide6.QtWidgets import QWidget, QListWidget
from PySide6.QtCore import Qt, QFile, QTextStream


class SupportWindowSidebar(QListWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("SupportWindowSidebar")
        self.setSpacing(5)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
