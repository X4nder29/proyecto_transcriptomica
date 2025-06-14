from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
    QLabel,
    QPushButton,
    QStyleOption,
    QStyle,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QIcon
from ....widgets.number_selector import NumberSelector


class SlidingWindowOption(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("SlidingWindowOption")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumWidth(350)

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):

        self.checkbox_icon_outlined = QIcon(":/assets/checkbox_outlined.svg")
        self.checkbox_icon_filled = QIcon(":/assets/checkbox_filled.svg")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # head

        self.title = QLabel("Sliding Window", self)
        self.title.setObjectName("OptionTitle")
        self.main_layout.addWidget(self.title)

        # body

        self.body = QWidget(self)
        self.body.setObjectName("OptionBody")

        self.body_layout = QVBoxLayout()
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(10)

        self.body.setLayout(self.body_layout)

        self.main_layout.addWidget(self.body)

        # window size suboption

        self.window_size_area = QWidget(self.body)
        self.window_size_area.setObjectName("SubOption")

        self.window_size_layout = QHBoxLayout(self.window_size_area)
        self.window_size_layout.setContentsMargins(0, 0, 0, 0)
        self.window_size_layout.setSpacing(10)

        self.window_size_button = QPushButton(self.window_size_area)
        self.window_size_button.setObjectName("Checkbox")
        self.window_size_button.setCheckable(True)
        self.window_size_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.window_size_button.setIcon(self.checkbox_icon_outlined)
        self.window_size_button.toggled.connect(
            lambda checked: self.update_icon(self.window_size_button, checked)
        )
        self.window_size_layout.addWidget(self.window_size_button)

        self.window_size_label = QLabel("Window Size", self.window_size_area)
        self.window_size_label.setObjectName("OptionLabel")
        self.window_size_layout.addWidget(self.window_size_label)

        self.window_size_selector = NumberSelector(self.window_size_area)
        self.window_size_selector.setObjectName("OptionNumberSelector")
        self.window_size_layout.addWidget(self.window_size_selector)

        self.body_layout.addWidget(self.window_size_area)

        # quality threshold suboption

        self.quality_threshold_area = QWidget(self.body)
        self.quality_threshold_area.setObjectName("SubOption")

        self.quality_threshold_layout = QHBoxLayout(self.quality_threshold_area)
        self.quality_threshold_layout.setContentsMargins(0, 0, 0, 0)
        self.quality_threshold_layout.setSpacing(10)

        self.quality_threshold_button = QPushButton(self.quality_threshold_area)
        self.quality_threshold_button.setObjectName("Checkbox")
        self.quality_threshold_button.setCheckable(True)
        self.quality_threshold_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.quality_threshold_button.setIcon(self.checkbox_icon_outlined)
        self.quality_threshold_button.toggled.connect(
            lambda checked: self.update_icon(self.quality_threshold_button, checked)
        )
        self.quality_threshold_layout.addWidget(self.quality_threshold_button)

        self.quality_threshold_label = QLabel("Quality Threshold", self.quality_threshold_area)
        self.quality_threshold_label.setObjectName("OptionLabel")
        self.quality_threshold_layout.addWidget(self.quality_threshold_label)

        self.quality_threshold_selector = NumberSelector(self.quality_threshold_area)
        self.quality_threshold_selector.setObjectName("OptionNumberSelector")
        self.quality_threshold_layout.addWidget(self.quality_threshold_selector)

        self.body_layout.addWidget(self.quality_threshold_area)

    def update_icon(self, button, checked):
        button.setIcon(
            self.checkbox_icon_filled if checked else self.checkbox_icon_outlined
        )

    def load_stylesheet(self):
        styles_path = Path(__file__).parent / "slidingwindow_option.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
        super().paintEvent(event)
