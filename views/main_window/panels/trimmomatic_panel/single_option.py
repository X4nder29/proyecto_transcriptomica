from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSizePolicy,
    QLabel,
    QPushButton,
    QStyleOption,
    QStyle,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QIcon
from ....widgets.number_selector import NumberSelector


class SingleOption(QWidget):

    def __init__(self, name: str, parent=None):
        super().__init__(parent)

        self.name = name

        self.setObjectName("SingleOption")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumWidth(300)

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):

        self.checkbox_icon_outlined = QIcon("assets/checkbox_outlined.svg")
        self.checkbox_icon_filled = QIcon("assets/checkbox_filled.svg")

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(5)

        self.leading_button = QPushButton(self)
        self.leading_button.setObjectName("Checkbox")
        self.leading_button.setCheckable(True)
        self.leading_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.leading_button.setIcon(self.checkbox_icon_outlined)
        self.leading_button.toggled.connect(
            lambda checked: self.update_icon(self.leading_button, checked)
        )

        self.leading_label = QLabel(self.name, self)
        self.leading_label.setObjectName("OptionLabel")
        self.leading_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.number_selector = NumberSelector(self)

        self.main_layout.addWidget(
            self.leading_button, alignment=Qt.AlignmentFlag.AlignLeft
        )
        self.main_layout.addWidget(
            self.leading_label, alignment=Qt.AlignmentFlag.AlignLeft
        )
        self.main_layout.addStretch()
        self.main_layout.addWidget(
            self.number_selector, alignment=Qt.AlignmentFlag.AlignRight
        )

    def load_stylesheet(self):
        styles_path = Path(__file__).parent / "single_option.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())

    def update_icon(self, button, checked):
        button.setIcon(
            self.checkbox_icon_filled if checked else self.checkbox_icon_outlined
        )

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
