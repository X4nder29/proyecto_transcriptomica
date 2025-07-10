from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QStyleOption,
    QStyle,
    QSizePolicy,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QFile, QTextStream
from .home_panel_head import HomePanelHead
from .home_panel_body import HomePanelBody


class HomePanel(QWidget):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("HomePanel")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.header = HomePanelHead(self)
        self.main_layout.addWidget(self.header, alignment=Qt.AlignmentFlag.AlignTop)

        self.content = HomePanelBody(self)
        self.main_layout.addWidget(self.content)

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
