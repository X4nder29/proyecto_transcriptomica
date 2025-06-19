from .option_widget import OptionWidget
from .number_selector_suboption_widget import NumberSelectorSuboptionWidget


class NumberSelectorOptionWidget(OptionWidget):
    def __init__(
        self, label: str, parent=None, checkable: bool = True, checked: bool = False
    ):
        self.label = label
        super().__init__(parent=parent, checkable=checkable, checked=checked)

    def setup_ui(self):
        super().setup_ui()
        self.checkbox.toggled.connect(self.toggle_suboption)
        self.number_selector_suboption_widget = NumberSelectorSuboptionWidget(
            self.label,
            parent=self,
        )
        self.number_selector_suboption_widget.setEnabled(self.checkbox.isChecked())
        self.main_layout.addWidget(self.number_selector_suboption_widget)

    def toggle_suboption(self, checked: bool):
        self.number_selector_suboption_widget.setEnabled(checked)
