from PySide6.QtWidgets import (
    QWidget,
    QSizePolicy,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt
from .decimal_selector import DecimalSelector
from .checkbox_widget import CheckBoxWidget


class DecimalSelectorSuboptionWidget(QWidget):
    def __init__(
        self,
        title: str,
        parent: QWidget = None,
        checkable: bool = False,
        checked: bool = False,
        decimals: int = 1,
        step: float = 0.1,
    ):
        super().__init__(parent)

        self.title = title
        self.checkable = checkable
        self.checked = checked
        self.decimals = decimals
        self.step = step

        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("SubOptionWidget")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        # checkbox
        if self.checkable:
            self.check_box_widget = CheckBoxWidget(self)
            self.check_box_widget.clicked.connect(self.toggle_suboption)
            self.main_layout.addWidget(
                self.check_box_widget, alignment=Qt.AlignmentFlag.AlignLeft
            )

        # label
        self.label = QLabel(self.title, self)
        self.label.setObjectName("SubOptionWidgetLabel")
        self.label.setToolTip("Enable or disable this option")
        self.main_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft)

        # spacer
        self.main_layout.addStretch(1)

        # number selector
        self.decimal_selector = DecimalSelector(
            self, decimals=self.decimals, step=self.step
        )
        self.decimal_selector.setEnabled(self.checked if self.checkable else True)
        self.main_layout.addWidget(
            self.decimal_selector, alignment=Qt.AlignmentFlag.AlignRight
        )

    def toggle_suboption(self, checked: bool):
        self.decimal_selector.setEnabled(checked)

    def value(self):
        return self.decimal_selector.value()

    def set_value(self, value: float):
        self.decimal_selector.set_value(value)

    def set_decimals(self, decimals: int):
        self.decimal_selector.set_decimals(decimals)

    def set_range(self, minimum: float, maximum: float):
        self.decimal_selector.set_range(minimum, maximum)

    def set_single_step(self, step: float):
        self.decimal_selector.set_single_step(step)
