from pathlib import Path
from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtCore import Qt, QFile, QTextStream


class ActionButtonWidget(QPushButton):
    def __init__(self, icon_path: str, tooltip: str, parent: QWidget = None):
        super().__init__(parent=parent)
        self.icon_path = icon_path
        self.tooltip = tooltip
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)
        QGuiApplication.styleHints().colorSchemeChanged.emit(
            QGuiApplication.styleHints().colorScheme()
        )

    def setup_ui(self):
        self.setObjectName("ActionButtonWidget")
        self.setToolTip(self.tooltip)
        self.setIcon(QIcon(self.icon_path))

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
            self.update()
            qss_file.close()
