from .option_widget import OptionWidget
from .decimal_selector_suboption_widget import DecimalSelectorSuboptionWidget


class DecimalSelectorOptionWidget(OptionWidget):

    def __init__(
        self,
        label: str,
        parent=None,
        checkable: bool = True,
        checked: bool = False,
        decimals: int = 1,
        step: float = 0.1,
    ):
        self.label = label
        self.decimals = decimals
        self.step = step
        super().__init__(parent=parent, checkable=checkable, checked=checked)

    def setup_ui(self):
        super().setup_ui()
        self.checkbox.toggled.connect(self.toggle_suboption)
        self.decimal_selector_suboption_widget = DecimalSelectorSuboptionWidget(
            self.label,
            parent=self,
            decimals=self.decimals,
            step=self.step,
        )
        self.decimal_selector_suboption_widget.setEnabled(self.checkbox.isChecked())
        self.main_layout.addWidget(self.decimal_selector_suboption_widget)

    def value(self):
        return self.decimal_selector_suboption_widget.value()

    def set_value(self, value: float):
        self.decimal_selector_suboption_widget.set_value(value)

    def set_range(self, minimum: float, maximum: float):
        self.decimal_selector_suboption_widget.set_range(minimum, maximum)

    def set_single_step(self, step: float):
        self.decimal_selector_suboption_widget.set_single_step(step)

    def toggle_suboption(self, checked: bool):
        self.decimal_selector_suboption_widget.setEnabled(checked)
