from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QPushButton,
    QStyleOption,
    QStyle,
    QLabel,
)
from PySide6.QtCore import Qt, QFile, QTextStream
from .home_panel_head import HomePanelHead
from .home_panel_body import HomePanelBody


class HomePanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("HomePanel")

        self.setupUi()

    def setupUi(self):
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        self.panel_head = HomePanelHead(self)
        self.main_layout.addWidget(self.panel_head, alignment=Qt.AlignmentFlag.AlignTop)

        self.panel_body = HomePanelBody(self)
        self.main_layout.addWidget(self.panel_body)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
