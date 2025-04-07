from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QLabel,
    QStyleOption,
    QStyle,
    QStackedLayout,
)
from PySide6.QtGui import QPainter
from ..panels.home_panel import HomePanel
from ..panels.graphics_panel import GraphicsPanel
from ..panels.settings_panel import SettingsPanel
from ..panels.trimmomatic_panel import TrimmomaticPanel


class Content(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("Content")
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self.setupUi()

    def setupUi(self):

        self.main_layout = QStackedLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setStyleSheet(
            """
            QWidget#Content {
                background-color: none;
            }
            """
        )

        self.home_panel = HomePanel(self)
        self.graphics_panel = GraphicsPanel(self)
        self.settings_panel = SettingsPanel(self)

        self.trimmomatic_panel = TrimmomaticPanel(self)

        self.main_layout.addWidget(self.home_panel)
        self.main_layout.addWidget(self.trimmomatic_panel)
        self.main_layout.addWidget(self.graphics_panel)
        self.main_layout.addWidget(self.settings_panel)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)