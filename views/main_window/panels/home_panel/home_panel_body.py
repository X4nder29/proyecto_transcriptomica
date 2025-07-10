from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QStyleOption,
    QStyle,
    QSizePolicy,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import QFile, QTextStream
from .widgets import CurrentWorkspace, WorkspaceFilesWidget


class HomePanelBody(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("HomePanelBody")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        self.current_workspace = CurrentWorkspace(self)
        self.main_layout.addWidget(self.current_workspace, 0, 0, 1, 1)

        self.files_area = WorkspaceFilesWidget(self)
        self.main_layout.addWidget(self.files_area, 1, 0, 2, 2)

        self.main_layout.setColumnStretch(1, 1)
        self.main_layout.setColumnStretch(2, 1)
        self.main_layout.setColumnStretch(3, 1)

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
