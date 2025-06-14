from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStyle, QStyleOption
from PySide6.QtGui import QPainter
from PySide6.QtCore import QFile, QTextStream
from pathlib import Path


class OptionArea(QWidget):
    """
    OptionArea is a QWidget that contains a list of options for the user to select from.
    It is used in the TrimmomaticPanel to allow the user to select different options for trimming.
    """

    def __init__(self, parent=None, title: str = None):
        super().__init__(parent)

        self.title = title

        self.setObjectName("OptionArea")

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        if self.title:
            self.title_label = QLabel(self.title, self)
            self.title_label.setObjectName("OptionTitle")
            self.main_layout.addWidget(self.title_label)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
