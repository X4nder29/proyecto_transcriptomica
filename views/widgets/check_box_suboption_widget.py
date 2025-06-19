from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt
from .checkbox_widget import CheckBoxWidget


class CheckBoxSuboptionWidget(QWidget):
    def __init__(self, title: str, parent=None, checked: bool = False):
        super().__init__(parent)
        self.title = title
        self.checked = checked
        self.setObjectName("CheckBoxSuboptionWidget")
        self.setMinimumWidth(300)
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        self.checkbox = CheckBoxWidget(self, checked=self.checked)
        self.main_layout.addWidget(self.checkbox, alignment=Qt.AlignmentFlag.AlignLeft)

        # label
        self.label = QLabel(self.title, self)
        self.label.setObjectName("SubOptionWidgetLabel")
        self.label.setToolTip("Enable or disable this option")
        self.main_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft)

        # spacer
        self.main_layout.addStretch(1)
