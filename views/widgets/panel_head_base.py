from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import QFile, QTextStream


class PanelHeadBase(QWidget):

    def __init__(self, title: str, parent: QWidget = None):
        super().__init__(parent=parent)
        self.title = title
        self.load_stylesheet()
        self.setup_ui()

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

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
