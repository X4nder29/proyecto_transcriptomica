from views.widgets import OptionWidget, NumberSelectorSuboptionWidget


class SlidingWindowOptionWidget(OptionWidget):
    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            title="Sliding Window",
        )

    def setup_ui(self):
        super().setup_ui()
        self.checkbox.clicked.connect(self.toggle_suboption)
        self.window_size_suboption = NumberSelectorSuboptionWidget(
            "Window Size",
            parent=self,
        )
        self.window_size_suboption.setEnabled(self.checkbox.isChecked())
        self.main_layout.addWidget(self.window_size_suboption)
        self.quality_threshold_suboption = NumberSelectorSuboptionWidget(
            "Quality Threshold",
            parent=self,
        )
        self.quality_threshold_suboption.setEnabled(self.checkbox.isChecked())
        self.main_layout.addWidget(self.quality_threshold_suboption)

    def toggle_suboption(self, checked: bool):
        self.window_size_suboption.setEnabled(checked)
        self.quality_threshold_suboption.setEnabled(checked)
