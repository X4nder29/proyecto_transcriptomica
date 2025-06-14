from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QLabel,
    QStyle,
    QStyleOption,
)
from PySide6.QtGui import QPainter, QIcon
from PySide6.QtCore import QSize, QFile, QTextStream
from PySide6.QtGui import QPainter
from pathlib import Path


class FileListItem(QWidget):

    def __init__(self, name, path, parent=None):
        super().__init__(parent)

        self.name = name
        self.path = path

        self.setObjectName("FileListItem")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
