from pathlib import Path
from PySide6.QtWidgets import QWidget, QDialog, QGridLayout, QStyleOption, QStyle
from PySide6.QtGui import QPainter, QIcon
from PySide6.QtCore import Qt, QFile, QTextStream
from .support_window_sidebar import SupportWindowSidebar
from .support_window_content import SupportWindowContent


class SupportWindow(QDialog):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Support Information")
        self.setWindowIcon(QIcon(":/assets/icon.svg"))
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.setWindowFlags(Qt.WindowType.Window)

        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.sidebar = SupportWindowSidebar(self)
        self.main_layout.addWidget(self.sidebar, 1, 0, 1, 1)

        self.content = SupportWindowContent(self)
        self.main_layout.addWidget(self.content, 1, 1, 1, 1)

        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 3)

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
