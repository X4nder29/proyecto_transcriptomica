from views.widgets import (
    OptionWidget,
    NumberSelectorSuboptionWidget,
    CheckBoxSuboptionWidget,
    ComboBoxSuboptionWidget,
)


class IlluminaClipOptionWidget(OptionWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent, title="Illumina Clip")

    def setup_ui(self):
        super().setup_ui()
        self.checkbox.toggled.connect(self.toggle_suboption)

        self.adaptar_suboption = ComboBoxSuboptionWidget("Adapter", parent=self)
        self.adaptar_suboption.setEnabled(self.checkbox.isChecked())
        self.main_layout.addWidget(self.adaptar_suboption)

        self.seed_mismatches_suboption = NumberSelectorSuboptionWidget(
            "Seed Mismatches", parent=self
        )
        self.seed_mismatches_suboption.setEnabled(self.checkbox.isChecked())
        self.main_layout.addWidget(self.seed_mismatches_suboption)

        self.palindrome_clip_threshold_suboption = NumberSelectorSuboptionWidget(
            "Palindrome Clip Threshold", parent=self
        )
        self.palindrome_clip_threshold_suboption.setEnabled(self.checkbox.isChecked())
        self.main_layout.addWidget(self.palindrome_clip_threshold_suboption)

        self.simple_clip_threshold_suboption = NumberSelectorSuboptionWidget(
            "Simple Clip Threshold", parent=self
        )
        self.simple_clip_threshold_suboption.setEnabled(self.checkbox.isChecked())
        self.main_layout.addWidget(self.simple_clip_threshold_suboption)

        self.min_adapter_length_suboption = NumberSelectorSuboptionWidget(
            "Minimum Adapter Length", parent=self, checkable=True
        )
        self.min_adapter_length_suboption.setEnabled(self.checkbox.isChecked())
        self.main_layout.addWidget(self.min_adapter_length_suboption)

        self.keep_both_reads_suboption = CheckBoxSuboptionWidget(
            "Keep Both Reads", self
        )
        self.keep_both_reads_suboption.setEnabled(self.checkbox.isChecked())
        self.main_layout.addWidget(self.keep_both_reads_suboption)

    def toggle_suboption(self, checked: bool):
        self.adaptar_suboption.setEnabled(checked)
        self.seed_mismatches_suboption.setEnabled(checked)
        self.palindrome_clip_threshold_suboption.setEnabled(checked)
        self.simple_clip_threshold_suboption.setEnabled(checked)
        self.min_adapter_length_suboption.setEnabled(checked)
        self.keep_both_reads_suboption.setEnabled(checked)
