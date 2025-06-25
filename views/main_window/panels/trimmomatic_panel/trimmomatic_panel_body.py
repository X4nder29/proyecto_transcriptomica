from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QSizePolicy,
    QStyleOption,
    QStyle,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import QFile, QTextStream
from views.widgets import (
    ThreadsSelectorWidget,
    SimpleInputFileWidget,
    PairedInputFileWidget,
    NumberSelectorOptionWidget,
    SegmentedOptionWidget,
    ConfigListWidget,
)
from .widgets import (
    IlluminaClipOptionWidget,
    SlidingWindowOptionWidget,
)


class TrimmomaticPanelBody(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("TrimmomaticPanelBody")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)
        self.setLayout(self.main_layout)

        from utils import OperationModes
        self.operation_mode_widget = SegmentedOptionWidget(
            "Operation Mode",
            [OperationModes.SingleEnd.value[0], OperationModes.PairedEnd.value[0]],
            self,
        )
        self.main_layout.addWidget(self.operation_mode_widget, 0, 0, 1, 1)

        self.simple_input_file_widget = SimpleInputFileWidget(self)
        self.main_layout.addWidget(self.simple_input_file_widget, 1, 0, 3, 1)

        self.paired_input_file_widget = PairedInputFileWidget(self)
        self.paired_input_file_widget.setVisible(False)
        self.main_layout.addWidget(self.paired_input_file_widget, 1, 0, 5, 1)

        self.threads_selector_widget = ThreadsSelectorWidget(self)
        self.main_layout.addWidget(self.threads_selector_widget, 0, 1, 1, 1)

        self.illumina_clip_option_widget = IlluminaClipOptionWidget(self)
        self.main_layout.addWidget(self.illumina_clip_option_widget, 1, 1, 7, 1)

        self.sliding_window_option_widget = SlidingWindowOptionWidget(self)
        self.main_layout.addWidget(self.sliding_window_option_widget, 8, 1, 3, 1)

        self.quality_scores_format_options_widget = SegmentedOptionWidget(
            "Quality Scores Format",
            ["Phred33", "Phred64"],
            self,
        )
        self.main_layout.addWidget(
            self.quality_scores_format_options_widget, 0, 2, 1, 1
        )

        self.leading_option_widget = NumberSelectorOptionWidget("Leading", self)
        self.main_layout.addWidget(self.leading_option_widget, 1, 2, 2, 1)

        self.trailing_option_widget = NumberSelectorOptionWidget("Trailing", self)
        self.main_layout.addWidget(self.trailing_option_widget, 3, 2, 2, 1)

        self.minlen_option_widget = NumberSelectorOptionWidget("Minlen", self)
        self.main_layout.addWidget(self.minlen_option_widget, 5, 2, 2, 1)

        self.crop_option_widget = NumberSelectorOptionWidget("Crop", self)
        self.main_layout.addWidget(self.crop_option_widget, 7, 2, 2, 1)

        self.headcrop_option_widget = NumberSelectorOptionWidget("Headcrop", self)
        self.main_layout.addWidget(self.headcrop_option_widget, 9, 2, 2, 1)

        self.config_list_widget = ConfigListWidget(self)
        self.main_layout.addWidget(self.config_list_widget, 0, 3, 11, 1)

        self.main_layout.setRowStretch(11, 1)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def paintEvent(self, _):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
        super().paintEvent(_)
