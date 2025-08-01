from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, QFile, QTextStream


class PanelHeadBase(QWidget):

    def __init__(self, title: str, parent: QWidget = None):
        super().__init__(parent=parent)
        self.title = title
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)
        QGuiApplication.styleHints().colorSchemeChanged.emit(
            QGuiApplication.styleHints().colorScheme()
        )

    def setup_ui(self):
        self.setObjectName("PanelHeadBase")

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)
        self.setLayout(self.main_layout)

        self.title_label = QLabel(self.title, self)
        self.title_label.setObjectName("TitleLabel")
        self.main_layout.addWidget(self.title_label)

        # add stretch

        self.main_layout.addStretch()

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
