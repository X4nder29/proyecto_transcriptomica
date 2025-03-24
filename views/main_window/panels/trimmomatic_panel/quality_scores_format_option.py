from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QButtonGroup,
    QLabel,
    QStyleOption,
    QStyle,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from pathlib import Path


class QualityScoresFormatOption(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("QualityScoresFormatOption")

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.title = QLabel("Quality Scores Format", self)
        self.title.setObjectName("OptionTitle")
        self.main_layout.addWidget(self.title)

        self.button_group_area = QWidget(self)
        self.button_group_area_layout = QHBoxLayout(self.button_group_area)
        self.button_group_area_layout.setContentsMargins(0, 0, 0, 0)
        self.button_group_area_layout.setSpacing(10)
        self.main_layout.addWidget(self.button_group_area)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        self.phred33_button = QPushButton("Phred 33", self.button_group_area)
        self.phred33_button.setCheckable(True)
        self.phred33_button.setChecked(True)
        self.button_group.addButton(self.phred33_button)
        self.button_group.setId(self.phred33_button, 33)
        self.button_group_area_layout.addWidget(self.phred33_button)

        self.phred64_button = QPushButton("Phred 64", self.button_group_area)
        self.phred64_button.setCheckable(True)
        self.button_group.addButton(self.phred64_button)
        self.button_group.setId(self.phred64_button, 64)
        self.button_group_area_layout.addWidget(self.phred64_button)

    def load_stylesheet(self):
        styles_path = Path(__file__).parent / "quality_scores_format_option.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
        super().paintEvent(event)
