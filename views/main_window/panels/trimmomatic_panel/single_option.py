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
from PySide6.QtCore import Qt, QFile, QTextStream
from PySide6.QtGui import QPainter, QIcon
from ....widgets.number_selector import NumberSelector


class SingleOption(QWidget):

    def __init__(self, name: str, parent=None, enabled: bool = True):
        super().__init__(parent)

        self.name = name
        self.enabled = enabled

        self.setObjectName("SingleOption")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumWidth(300)

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):

        self.checkbox_icon_outlined = QIcon(":/assets/checkbox_outlined.svg")
        self.checkbox_icon_filled = QIcon(":/assets/checkbox_filled.svg")

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(5)

        self.leading_button = QPushButton(self)
        self.leading_button.setObjectName("Checkbox")
        self.leading_button.setCheckable(True)
        self.leading_button.setChecked(self.enabled)
        self.leading_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.leading_button.setIcon(self.checkbox_icon_outlined if not self.enabled else self.checkbox_icon_filled)
        self.leading_button.toggled.connect(
            lambda checked: self.leading_button_toggled(checked)
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

    def leading_button_toggled(self, checked):
        self.number_selector.setEnabled(checked)
        self.update_icon(self.leading_button, checked)

    def update_icon(self, button, checked):
        button.setIcon(
            self.checkbox_icon_filled if checked else self.checkbox_icon_outlined
        )

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
