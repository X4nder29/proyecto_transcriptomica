from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QStyle,
    QStyleOption,
    QPushButton,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from pathlib import Path
from .graphic import Graphic


class Section2(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("Section3")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_style_sheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.per_base_sequence_quality = QPushButton("Per base sequence quality", self)
        self.per_base_sequence_quality.setObjectName("SectionButton")
        self.main_layout.addWidget(self.per_base_sequence_quality, alignment=Qt.AlignmentFlag.AlignTop)

        self.per_sequence_quality_scores = QPushButton("Per sequence quality scores", self)
        self.per_sequence_quality_scores.setObjectName("SectionButton")
        self.main_layout.addWidget(self.per_sequence_quality_scores, alignment=Qt.AlignmentFlag.AlignTop)

        self.per_base_sequence_content = QPushButton("Per base sequence content", self)
        self.per_base_sequence_content.setObjectName("SectionButton")
        self.main_layout.addWidget(self.per_base_sequence_content, alignment=Qt.AlignmentFlag.AlignTop)

        self.per_sequence_gc_content = QPushButton("Per sequence GC content", self)
        self.per_sequence_gc_content.setObjectName("SectionButton")
        self.main_layout.addWidget(self.per_sequence_gc_content, alignment=Qt.AlignmentFlag.AlignTop)

        self.per_base_n_content = QPushButton("Per base N content", self)
        self.per_base_n_content.setObjectName("SectionButton")
        self.main_layout.addWidget(self.per_base_n_content, alignment=Qt.AlignmentFlag.AlignTop)

        self.sequence_length_distribution = QPushButton("Sequence length distribution", self)
        self.sequence_length_distribution.setObjectName("SectionButton")
        self.main_layout.addWidget(self.sequence_length_distribution, alignment=Qt.AlignmentFlag.AlignTop)

        self.duplication_levels = QPushButton("Duplication levels", self)
        self.duplication_levels.setObjectName("SectionButton")
        self.main_layout.addWidget(self.duplication_levels, alignment=Qt.AlignmentFlag.AlignTop)

        self.overrepresented_sequences = QPushButton("Overrepresented sequences", self)
        self.overrepresented_sequences.setObjectName("SectionButton")
        self.main_layout.addWidget(self.overrepresented_sequences, alignment=Qt.AlignmentFlag.AlignTop)

        self.adapter_content = QPushButton("Adapter content", self)
        self.adapter_content.setObjectName("SectionButton")
        self.main_layout.addWidget(self.adapter_content, alignment=Qt.AlignmentFlag.AlignTop)

        self.main_layout.addStretch(1)

    def load_style_sheet(self):
        styles_path = Path(__file__).parent / "section_2.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)