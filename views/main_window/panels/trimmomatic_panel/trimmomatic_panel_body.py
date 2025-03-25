from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QStackedLayout,
    QSizePolicy,
    QLabel,
)
from PySide6.QtCore import Qt
from .mode_area import ModeArea
from .se_files_area import SeFilesArea
from .pe_files_area import PeFilesArea
from .threads_options import ThreadsOption
from .quality_scores_format_option import QualityScoresFormatOption
from .single_option import SingleOption
from .illumina_clip_option import IlluminaClipOption
from .slidingwindow_option import SlidingWindowOption


class TrimmomaticPanelBody(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("TrimmomaticPanelBody")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.loadStylesheet()

        self.setupUi()

    def setupUi(self):

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        # left section

        self.left_section = QWidget(self)
        self.left_section.setObjectName("LeftSection")
        self.left_section.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.left_section.setMinimumWidth(300)

        self.left_section_layout = QVBoxLayout(self.left_section)
        self.left_section_layout.setContentsMargins(0, 0, 0, 0)
        self.left_section_layout.setSpacing(20)

        self.mode_area = ModeArea(self.left_section)
        self.mode_area.button_group.idClicked.connect(lambda id: self.changeMode(id))

        self.files_areas = QWidget(self.left_section)
        self.files_areas_layout = QStackedLayout(self.files_areas)

        self.files_area_se = SeFilesArea(self.left_section)
        self.files_area_pe = PeFilesArea(self.left_section)

        self.files_areas_layout.addWidget(self.files_area_se)
        self.files_areas_layout.addWidget(self.files_area_pe)

        self.left_section_layout.addWidget(self.mode_area, alignment=Qt.AlignmentFlag.AlignTop)
        self.left_section_layout.addWidget(self.files_areas, alignment=Qt.AlignmentFlag.AlignTop)
        self.left_section_layout.addStretch()

        ## center section

        self.center_section = QWidget(self)
        self.center_section.setObjectName("CenterSection")

        self.center_section_layout = QGridLayout(self.center_section)
        self.center_section_layout.setContentsMargins(0, 0, 0, 0)
        self.center_section_layout.setSpacing(20)

        self.threads_option = ThreadsOption(self.center_section)
        self.quality_scores_format_option = QualityScoresFormatOption(self.center_section)
        self.illumina_clip_option = IlluminaClipOption(self.center_section)
        self.slidingwindow_option = SlidingWindowOption(self.center_section)
        self.leading_option = SingleOption("Leading", self.center_section)
        self.trailing_option = SingleOption("Trailing", self.center_section)
        self.minlen_option = SingleOption("Minlen", self.center_section)
        self.crop_option = SingleOption("Crop", self.center_section)
        self.headcrop_option = SingleOption("Headcrop", self.center_section)

        self.center_section_layout.addWidget(self.threads_option, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)
        self.center_section_layout.addWidget(self.quality_scores_format_option, 0, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)

        self.center_section_layout.addWidget(self.illumina_clip_option, 1, 0, 4, 1, alignment=Qt.AlignmentFlag.AlignTop)
        self.center_section_layout.addWidget(self.slidingwindow_option, 5, 0, 2, 1, alignment=Qt.AlignmentFlag.AlignTop)

        self.center_section_layout.addWidget(self.leading_option, 1, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)
        self.center_section_layout.addWidget(self.trailing_option, 2, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)
        self.center_section_layout.addWidget(self.minlen_option, 3, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)
        self.center_section_layout.addWidget(self.crop_option, 4, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)
        self.center_section_layout.addWidget(self.headcrop_option, 5, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)

        ## right section

        self.right_section = QWidget(self)
        self.right_section.setObjectName("RightSection")
        self.right_section.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )
        self.right_section.setMinimumWidth(300)

        self.right_section_layout = QVBoxLayout(self.right_section)
        self.right_section_layout.setContentsMargins(0, 0, 0, 0)
        self.right_section_layout.setSpacing(0)

        self.right_section_label = QLabel("Configuraciones\nGuardadas", self.right_section)
        self.right_section_label.setObjectName("RightSectionLabel")

        self.right_section_layout.addWidget(self.right_section_label, alignment=Qt.AlignmentFlag.AlignTop)

        # add areas

        self.main_layout.addWidget(self.left_section)
        self.main_layout.addWidget(self.center_section, alignment=Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.right_section)

    def loadStylesheet(self):
        styles_path = Path(__file__).parent / "trimmomatic_panel_body.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())

    def changeMode(self, id):
        self.files_areas_layout.setCurrentIndex(id)
