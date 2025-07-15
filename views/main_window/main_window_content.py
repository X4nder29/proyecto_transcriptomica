from ctypes import alignment
from PySide6.QtWidgets import (
    QWidget,
    QSizePolicy,
    QStyleOption,
    QStyle,
    QStackedLayout,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from ..widgets import WorkInProgressPosterPanel
from .panels.home_panel import HomePanel
from .panels.graphics_panel import GraphicsPanel
from .panels.settings_panel import SettingsPanel
from .panels.trimmomatic_panel import TrimmomaticPanel
from .panels.fastqc_panel import FastqcPanel
from controllers.trimmomatic_panel_controller import TrimmomaticPanelController


class MainWindowContent(QWidget):

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

        self.main_layout.setCurrentIndex(1)

        # panels
        # home panel

        self.home_panel = HomePanel(self)
        # fastqc panel

        from controllers import FastQCPanelController

        self.fastqc_panel = FastqcPanel(self)
        self.fastqc_panel_controller = FastQCPanelController(self.fastqc_panel)
        self.main_layout.addWidget(self.fastqc_panel)

        # trimmomatic panel

        from controllers import TrimmomaticPanelController

        self.trimmomatic_panel = TrimmomaticPanel(self)
        self.trimmomatic_panel_controller = TrimmomaticPanelController(
            self.trimmomatic_panel
        )
        self.main_layout.addWidget(self.trimmomatic_panel)

        # sort me rna panel

        self.sort_me_rna = WorkInProgressPosterPanel(self)

        # kraken2 panel

        from controllers import KrakenPanelController

        self.kraken2 = KrakenPanel(self)
        self.kraken2_controller = KrakenPanelController(self.kraken2)
        self.main_layout.addWidget(self.kraken2)

        # settings panel

        self.settings_panel = SettingsPanel(self)

        # add panels to the main layout

        self.main_layout.addWidget(self.home_panel)
        self.main_layout.addWidget(self.trimmomatic_panel)
        self.main_layout.addWidget(self.sort_me_rna)
        self.main_layout.addWidget(self.kraken2)
        self.main_layout.addWidget(self.fastqc_panel)
        self.main_layout.addWidget(self.settings_panel)

    def paintEvent(self, _):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
