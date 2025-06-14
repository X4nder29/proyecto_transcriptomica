from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)
from PySide6.QtCore import QFile, QTextStream


class HomePanelBody(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("HomePanelBody")

        self.load_stylesheet()

        self.setupUi()

    def setupUi(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.programs_area = ProgramsArea(self)
        self.main_layout.addWidget(self.programs_area, alignment=Qt.AlignmentFlag.AlignRight)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
