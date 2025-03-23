from pathlib import Path
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
    QPushButton,
)
from PySide6.QtGui import QPainter, QIcon
from PySide6.QtCore import Qt
from ....widgets.number_selector import NumberSelector


class IlluminaClipOption(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("IlluminaClipOption")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumWidth(350)

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):

        """ 
        self.setMinimumHeight(175) """

        self.checkbox_icon_outlined = QIcon("assets/checkbox_outlined.svg")
        self.checkbox_icon_filled = QIcon("assets/checkbox_filled.svg")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # head

        self.title = QLabel("Illumina Clip", self)
        self.title.setObjectName("title")

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
        self.adapter_area_layout.setSpacing(10)

        self.adapter_button = QPushButton(self.body)
        self.adapter_button.setObjectName("checkbox")
        self.adapter_button.setCheckable(True)
        self.adapter_button.setIcon(self.checkbox_icon_outlined)
        self.adapter_button.toggled.connect(
            lambda checked: self.update_icon(self.adapter_button, checked)
        )
        self.adapter_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.adapter_area_layout.addWidget(self.adapter_button)

        self.adapter_label = QLabel("Adapter", self.body)
        self.adapter_label.setObjectName("adapter_label")

        self.adapter_area_layout.addWidget(self.adapter_label)

        self.adapter_options = QComboBox(self.body)
        self.adapter_options.setObjectName("adapter_options")
        self.adapter_options.addItems(["TruSeq2-PE.fa", "TruSeq3-PE.fa", "NexteraPE-PE.fa"])

        self.adapter_area_layout.addWidget(self.adapter_options)

        self.body_layout.addWidget(self.adapter_area)

        # seed mismatches suboption

        self.seed_mismatches_area = QWidget(self.body)
        self.seed_mismatches_area.setObjectName("seed_mismatches_area")

        self.seed_mismatches_area_layout = QHBoxLayout(self.seed_mismatches_area)
        self.seed_mismatches_area_layout.setContentsMargins(0, 0, 0, 0)
        self.seed_mismatches_area_layout.setSpacing(10)

        self.seed_mismatches_button = QPushButton(self.seed_mismatches_area)
        self.seed_mismatches_button.setObjectName("checkbox")
        self.seed_mismatches_button.setCheckable(True)
        self.seed_mismatches_button.setIcon(self.checkbox_icon_outlined)
        self.seed_mismatches_button.toggled.connect(
            lambda checked: self.update_icon(self.seed_mismatches_button, checked)
        )
        self.seed_mismatches_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.seed_mismatches_area_layout.addWidget(self.seed_mismatches_button)

        self.seed_mismatches_label = QLabel("Seed Mismatches", self.body)
        self.seed_mismatches_label.setObjectName("seed_mismatches_label")

        self.seed_mismatches_area_layout.addWidget(self.seed_mismatches_label)

        self.seed_mismatches_input = NumberSelector(self.seed_mismatches_area)

        self.seed_mismatches_area_layout.addWidget(self.seed_mismatches_input)

        self.body_layout.addWidget(self.seed_mismatches_area)

        # palindrome clip threshold suboption

        self.palindrome_clip_threshold_area = QWidget(self.body)
        self.palindrome_clip_threshold_area.setObjectName("palindrome_clip_threshold_area")

        self.palindrome_clip_threshold_area_layout = QHBoxLayout(self.palindrome_clip_threshold_area)
        self.palindrome_clip_threshold_area_layout.setContentsMargins(0, 0, 0, 0)
        self.palindrome_clip_threshold_area_layout.setSpacing(10)

        self.palindrome_clip_threshold_button = QPushButton(
            self.palindrome_clip_threshold_area
        )
        self.palindrome_clip_threshold_button.setObjectName("checkbox")
        self.palindrome_clip_threshold_button.setCheckable(True)
        self.palindrome_clip_threshold_button.setIcon(self.checkbox_icon_outlined)
        self.palindrome_clip_threshold_button.toggled.connect(
            lambda checked: self.update_icon(self.palindrome_clip_threshold_button, checked)
        )
        self.palindrome_clip_threshold_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.palindrome_clip_threshold_area_layout.addWidget(self.palindrome_clip_threshold_button)

        self.palindrome_clip_threshold_label = QLabel(
            "Palindrome Clip Threshold", self.palindrome_clip_threshold_area
        )
        self.palindrome_clip_threshold_label.setObjectName("palindrome_clip_threshold_label")

        self.palindrome_clip_threshold_area_layout.addWidget(self.palindrome_clip_threshold_label)

        self.palindrome_clip_threshold_input = NumberSelector(
            self.palindrome_clip_threshold_area
        )

        self.palindrome_clip_threshold_area_layout.addWidget(self.palindrome_clip_threshold_input)

        self.body_layout.addWidget(self.palindrome_clip_threshold_area)

        # simple clip threshold suboption

        self.simple_clip_threshold_area = QWidget(self.body)
        self.simple_clip_threshold_area.setObjectName("simple_clip_threshold_area")

        self.simple_clip_threshold_area_layout = QHBoxLayout(self.simple_clip_threshold_area)
        self.simple_clip_threshold_area_layout.setContentsMargins(0, 0, 0, 0)
        self.simple_clip_threshold_area_layout.setSpacing(10)

        self.simple_clip_threshold_button = QPushButton(self.simple_clip_threshold_area)
        self.simple_clip_threshold_button.setObjectName("checkbox")
        self.simple_clip_threshold_button.setCheckable(True)
        self.simple_clip_threshold_button.setIcon(self.checkbox_icon_outlined)
        self.simple_clip_threshold_button.toggled.connect(
            lambda checked: self.update_icon(self.simple_clip_threshold_button, checked)
        )
        self.simple_clip_threshold_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.simple_clip_threshold_area_layout.addWidget(self.simple_clip_threshold_button)

        self.simple_clip_threshold_label = QLabel(
            "Simple Clip Threshold", self.simple_clip_threshold_area
        )
        self.simple_clip_threshold_label.setObjectName("simple_clip_threshold_label")

        self.simple_clip_threshold_area_layout.addWidget(self.simple_clip_threshold_label)

        self.simple_clip_threshold_input = NumberSelector(
            self.simple_clip_threshold_area
        )

        self.simple_clip_threshold_area_layout.addWidget(self.simple_clip_threshold_input)

        self.body_layout.addWidget(self.simple_clip_threshold_area)

        # min adapter length suboption

        self.min_adapter_length_area = QWidget(self.body)
        self.min_adapter_length_area.setObjectName("min_adapter_length_area")

        self.min_adapter_length_area_layout = QHBoxLayout(self.min_adapter_length_area)
        self.min_adapter_length_area_layout.setContentsMargins(0, 0, 0, 0)
        self.min_adapter_length_area_layout.setSpacing(10)

        self.min_adapter_length_button = QPushButton(self.min_adapter_length_area)
        self.min_adapter_length_button.setObjectName("checkbox")
        self.min_adapter_length_button.setCheckable(True)
        self.min_adapter_length_button.setIcon(self.checkbox_icon_outlined)
        self.min_adapter_length_button.toggled.connect(
            lambda checked: self.update_icon(self.min_adapter_length_button, checked)
        )
        self.min_adapter_length_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.min_adapter_length_area_layout.addWidget(self.min_adapter_length_button)

        self.min_adapter_length_label = QLabel(
            "Min Adapter Length", self.min_adapter_length_area
        )
        self.min_adapter_length_label.setObjectName("min_adapter_length_label")
        self.min_adapter_length_area_layout.addWidget(self.min_adapter_length_label)

        self.min_adapter_length_selector = NumberSelector(self.min_adapter_length_area)
        self.min_adapter_length_area_layout.addWidget(self.min_adapter_length_selector)

        self.body_layout.addWidget(self.min_adapter_length_area)

        # keep both reads suboption

        self.keep_both_reads_area = QWidget(self.body)
        self.keep_both_reads_area.setObjectName("keep_both_reads_area")

        self.keep_both_reads_area_layout = QHBoxLayout(self.keep_both_reads_area)
        self.keep_both_reads_area_layout.setContentsMargins(0, 0, 0, 0)
        self.keep_both_reads_area_layout.setSpacing(10)

        self.keep_both_reads_button = QPushButton(self.body)
        self.keep_both_reads_button.setObjectName("checkbox")
        self.keep_both_reads_button.setCheckable(True)
        self.keep_both_reads_button.setIcon(self.checkbox_icon_outlined)
        self.keep_both_reads_button.toggled.connect(
            lambda checked: self.update_icon(self.keep_both_reads_button, checked)
        )
        self.keep_both_reads_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.keep_both_reads_area_layout.addWidget(self.keep_both_reads_button)

        self.keep_both_reads_label = QLabel("Keep Both Reads", self.body)
        self.keep_both_reads_label.setObjectName("keep_both_reads_label")
        self.keep_both_reads_area_layout.addWidget(self.keep_both_reads_label)

        self.body_layout.addWidget(self.keep_both_reads_area)

    def load_stylesheet(self):
        styles_path = Path(__file__).parent / "illumina_clip_option.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())

    def update_icon(self, button, checked):
        button.setIcon(self.checkbox_icon_filled if checked else self.checkbox_icon_outlined)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
