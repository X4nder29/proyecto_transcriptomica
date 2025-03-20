from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QSizePolicy,
    QLabel,
    QStyleOption,
    QStyle,
    QComboBox,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from .number_selector import NumberSelector


class IlluminaClipOption(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("IlluminaClipOption")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setupUi()

    def setupUi(self):

        self.setMinimumWidth(350)
        self.setMinimumHeight(175)
        self.setStyleSheet(
            """
            QWidget#IlluminaClipOption {
                background-color: #404040;
                border-radius: 10px;
            }
            """
        )

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # head

        self.title = QLabel("Illumina Clip", self)
        self.title.setObjectName("title")
        self.title.setStyleSheet(
            """
            QLabel#title {
                font-size: 14px;
                font-weight: bold;
                color: white;
            }
            """
        )

        self.main_layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignTop)

        # body

        self.body = QWidget(self)
        self.body.setObjectName("body")

        self.body_layout = QGridLayout(self.body)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(10)

        self.main_layout.addWidget(self.body)

        # adapter suboption

        self.adapter_area = QWidget(self.body)
        self.adapter_area.setObjectName("adapter_area")

        self.adapter_area_layout = QHBoxLayout(self.adapter_area)
        self.adapter_area_layout.setContentsMargins(0, 0, 0, 0) 
        self.adapter_area_layout.setSpacing(20)

        self.adapter_label = QLabel("Adapter", self.body)
        self.adapter_label.setObjectName("adapter_label")
        self.adapter_label.setStyleSheet(
            """
            QLabel#adapter_label {
                font-size: 12px;
                color: white;
            }
            """
        )

        self.adapter_area_layout.addWidget(self.adapter_label)

        self.adapter_options = QComboBox(self.body)
        self.adapter_options.setObjectName("adapter_options")
        self.adapter_options.setStyleSheet(
            """
            QComboBox#adapter_options {
                background-color: none;
                border-radius: 5px;
                padding: 0.5em;
            }
            /*QComboBox#adapter_options::drop-down {
                border: none;
            }*/
            """
        )
        self.adapter_options.addItems(["TruSeq2-PE.fa", "TruSeq3-PE.fa", "NexteraPE-PE.fa"])

        self.adapter_area_layout.addWidget(self.adapter_options)

        self.body_layout.addWidget(self.adapter_area)

        # seed mismatches suboption

        self.seed_mismatches_area = QWidget(self.body)
        self.seed_mismatches_area.setObjectName("seed_mismatches_area")

        self.seed_mismatches_area_layout = QHBoxLayout(self.seed_mismatches_area)
        self.seed_mismatches_area_layout.setContentsMargins(0, 0, 0, 0)
        self.seed_mismatches_area_layout.setSpacing(20)

        self.seed_mismatches_label = QLabel("Seed Mismatches", self.body)
        self.seed_mismatches_label.setObjectName("seed_mismatches_label")
        self.seed_mismatches_label.setStyleSheet(
            """
            QLabel#seed_mismatches_label {
                font-size: 12px;
                color: white;
            }
            """
        )

        self.seed_mismatches_area_layout.addWidget(self.seed_mismatches_label)

        self.seed_mismatches_input = NumberSelector(self.body)

        self.seed_mismatches_area_layout.addWidget(self.seed_mismatches_input)

        self.body_layout.addWidget(self.seed_mismatches_area)

        # palindrome clip threshold suboption

        self.palindrome_clip_threshold_area = QWidget(self.body)
        self.palindrome_clip_threshold_area.setObjectName("palindrome_clip_threshold_area")

        self.palindrome_clip_threshold_area_layout = QHBoxLayout(self.palindrome_clip_threshold_area)
        self.palindrome_clip_threshold_area_layout.setContentsMargins(0, 0, 0, 0)
        self.palindrome_clip_threshold_area_layout.setSpacing(20)

        self.palindrome_clip_threshold_label = QLabel("Palindrome Clip Threshold", self.body)
        self.palindrome_clip_threshold_label.setObjectName("palindrome_clip_threshold_label")
        self.palindrome_clip_threshold_label.setStyleSheet(
            """
            QLabel#palindrome_clip_threshold_label {
                font-size: 12px;
                color: white;
            }
            """
        )

        self.palindrome_clip_threshold_area_layout.addWidget(self.palindrome_clip_threshold_label)

        self.palindrome_clip_threshold_input = NumberSelector(self.body)

        self.palindrome_clip_threshold_area_layout.addWidget(self.palindrome_clip_threshold_input)

        self.body_layout.addWidget(self.palindrome_clip_threshold_area)
        

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
