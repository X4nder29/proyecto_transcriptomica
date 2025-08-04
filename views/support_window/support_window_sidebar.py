from pathlib import Path
from PySide6.QtWidgets import QWidget, QListWidget
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, QFile, QTextStream


class SupportWindowSidebar(QListWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)
        self.load_stylesheet(QGuiApplication.styleHints().colorScheme())
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)

    def setup_ui(self):
        self.setObjectName("SupportWindowSidebar")
        self.setSpacing(5)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def load_stylesheet(self, scheme: Qt.ColorScheme):
        qss_file = QFile(
            f":/styles/{Path(__file__).stem}_{"dark" if scheme == Qt.ColorScheme.Dark else "light"}.qss"
        )
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            style = self.style()
            style.unpolish(self)
            style.polish(self)
            qss_file.close()
