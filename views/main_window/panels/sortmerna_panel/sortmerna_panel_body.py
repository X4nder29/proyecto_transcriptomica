from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QStackedWidget,
    QStyleOption,
    QStyle,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import QFile, QTextStream
from views.widgets import GenerationPage
from .pages import FilesPage, OptionsPage


class SortMeRnaPanelBody(QStackedWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("SortMeRnaBodyPanel")

        self.files_page = FilesPage(self)
        self.addWidget(self.files_page)

        self.options_page = OptionsPage(self)
        self.addWidget(self.options_page)

        self.generation_page = GenerationPage(self)
        self.addWidget(self.generation_page)

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
        super().paintEvent(event)
