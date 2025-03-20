from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QSizePolicy,
    QLabel,
)
from .bioinformatic.trimmomatic_options.illumina_clip_option import IlluminaClipOption
from .bioinformatic.trimmomatic_options.leading_option import LeadingOption
from .bioinformatic.trimmomatic_options.trailing_option import TrailingOption
from .bioinformatic.trimmomatic_options.slidingwindow_option import SlidingWindowOption
from .bioinformatic.trimmomatic_options.minlen_option import MinlenOption


class BioinformaticPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("BioinformaticPanel")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        self.setupUi()

    def setupUi(self):

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # trimmomatic area

        self.trimmomatic_area = QWidget(self)
        self.trimmomatic_area.setObjectName("trimmomatic_area")

        self.trimmomatic_area_layout = QVBoxLayout(self.trimmomatic_area)
        self.trimmomatic_area_layout.setContentsMargins(0, 0, 0, 0)
        self.trimmomatic_area_layout.setSpacing(10)

        self.trimmomatic_label = QLabel("Trimmomatic", self.trimmomatic_area)
        self.trimmomatic_label.setObjectName("trimmomatic_label")
        self.trimmomatic_label.setStyleSheet(
            """
            QLabel#trimmomatic_label {
                font-size: 20px;
                font-weight: bold;
            }
            """
        )

        self.trimmomatic_area_layout.addWidget(self.trimmomatic_label)

        self.trimmomatic_body = QWidget(self.trimmomatic_area)
        self.trimmomatic_body.setObjectName("trimmomatic_body")

        self.trimmomatic_body_layout = QGridLayout(self.trimmomatic_body)
        self.trimmomatic_body_layout.setContentsMargins(0, 0, 0, 0)
        self.trimmomatic_body_layout.setSpacing(10)

        self.trimmomatic_area_layout.addWidget(self.trimmomatic_body)

        self.illumina_clip_option = IlluminaClipOption(self.trimmomatic_body)

        self.sliding_window_option = SlidingWindowOption(self.trimmomatic_body)

        self.leading_option = LeadingOption(self.trimmomatic_body)

        self.trailing_option = TrailingOption(self.trimmomatic_body)

        self.minlen_option = MinlenOption(self.trimmomatic_body)

        self.trimmomatic_body_layout.addWidget(self.illumina_clip_option, 0, 0, 3, 1)
        self.trimmomatic_body_layout.addWidget(self.sliding_window_option, 0, 1, 3, 1)
        self.trimmomatic_body_layout.addWidget(self.leading_option, 0, 2, 1, 1)
        self.trimmomatic_body_layout.addWidget(self.trailing_option, 1, 2, 1, 1)
        self.trimmomatic_body_layout.addWidget(self.minlen_option, 2, 2, 1, 1)

        self.main_layout.addWidget(self.trimmomatic_area)

        # sort rna area

        self.sort_rna_area = QWidget(self)
        self.sort_rna_area.setObjectName("sort_rna_area")

        self.sort_rna_area_layout = QVBoxLayout(self.sort_rna_area)
        self.sort_rna_area_layout.setContentsMargins(0, 0, 0, 0)
        self.sort_rna_area_layout.setSpacing(0)

        self.sort_rna_label = QLabel("Sort RNA", self.sort_rna_area)
        self.sort_rna_label.setObjectName("sort_rna_label")
        self.sort_rna_label.setStyleSheet(
            """
            QLabel#sort_rna_label {
                font-size: 20px;
                font-weight: bold;
            }
            """
        )

        self.sort_rna_area_layout.addWidget(self.sort_rna_label)

        self.sort_rna_body = QWidget(self.sort_rna_area)
        self.sort_rna_body.setObjectName("sort_rna_body")

        self.sort_rna_body_layout = QGridLayout(self.sort_rna_body)
        self.sort_rna_body_layout.setContentsMargins(0, 0, 0, 0)
        self.sort_rna_body_layout.setSpacing(0)

        self.sort_rna_area_layout.addWidget(self.sort_rna_body)

        self.bento4 = QLabel("bento4", self.sort_rna_body)

        self.bento4.setObjectName("bento4")
        self.bento4.setStyleSheet(
            "QWidget#bento4 { background-color: orange; }"
        )

        self.bento5 = QLabel("bento5", self.sort_rna_body)
        self.bento5.setObjectName("bento5")
        self.bento5.setStyleSheet(
            "QWidget#bento5 { background-color: purple; }"
        )

        self.bento6 = QLabel("bento6", self.sort_rna_body)
        self.bento6.setObjectName("bento6")
        self.bento6.setStyleSheet(
            "QWidget#bento6 { background-color: pink; }"
        )

        self.sort_rna_body_layout.addWidget(self.bento4, 0, 0, 1, 1)
        self.sort_rna_body_layout.addWidget(self.bento5, 0, 1, 1, 1)
        self.sort_rna_body_layout.addWidget(self.bento6, 0, 2, 1, 2)

        self.main_layout.addWidget(self.sort_rna_area)

        # kraken area

        self.kraken_area = QWidget(self)
        self.kraken_area.setObjectName("kraken_area")

        self.kraken_area_layout = QVBoxLayout(self.kraken_area)
        self.kraken_area_layout.setContentsMargins(0, 0, 0, 0)
        self.kraken_area_layout.setSpacing(0)

        self.kraken_label = QLabel("Kraken", self.kraken_area)
        self.kraken_label.setObjectName("kraken_label")
        self.kraken_label.setStyleSheet(
            """
            QLabel#kraken_label {
                font-size: 20px;
                font-weight: bold;
            }
            """
        )

        self.kraken_area_layout.addWidget(self.kraken_label)

        self.kraken_body = QWidget(self.kraken_area)
        self.kraken_body.setObjectName("kraken_body")

        self.kraken_body_layout = QGridLayout(self.kraken_body)
        self.kraken_body_layout.setContentsMargins(0, 0, 0, 0)
        self.kraken_body_layout.setSpacing(0)

        self.kraken_area_layout.addWidget(self.kraken_body)

        self.bento7 = QLabel("bento7", self.kraken_body)
        self.bento7.setObjectName("bento7")
        self.bento7.setStyleSheet(
            "QWidget#bento7 { background-color: blue; }"
        )

        self.bento8 = QLabel("bento8", self.kraken_body)
        self.bento8.setObjectName("bento8")
        self.bento8.setStyleSheet(
            "QWidget#bento8 { background-color: green; }"
        )

        self.bento9 = QLabel("bento9", self.kraken_body)
        self.bento9.setObjectName("bento9")
        self.bento9.setStyleSheet(
            "QWidget#bento9 { background-color: yellow; }"
        )

        self.kraken_body_layout.addWidget(self.bento7, 0, 0, 1, 1)
        self.kraken_body_layout.addWidget(self.bento8, 0, 1, 1, 1)
        self.kraken_body_layout.addWidget(self.bento9, 0, 2, 1, 2)

        self.main_layout.addWidget(self.kraken_area)
