from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QStyle,
    QStyleOption,
)
from PySide6.QtGui import QIcon, QPainter
from PySide6.QtCore import QFile, QTextStream
from .home_window_body import HomeWindowBody


class HomeWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("TranscriptoHub")
        self.setWindowIcon(QIcon(":/assets/icon.svg"))
        self.setMinimumSize(1000, 600)
        self.setAcceptDrops(True)

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):

        self.setObjectName("HomeWindow")

        # central widget

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)

        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)

        # body

        self.body = HomeWindowBody(self)
        self.body.setObjectName("Body")
        self.central_layout.addWidget(self.body)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def paintEvent(self, _):
        option = QStyleOption()
        option.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)
