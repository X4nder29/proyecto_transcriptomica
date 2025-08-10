from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QHBoxLayout,
    QStyleOption,
    QStyle,
    QSizePolicy,
    QLabel,
    QPushButton,
    QHBoxLayout,
)
from PySide6.QtGui import QGuiApplication, QPainter
from PySide6.QtCore import Qt, QFile, QTextStream
from views.widgets import (
    ThreadsSelectorWidget,
    NumberSelectorOptionWidget,
    SegmentedOptionWidget,
    ListWidget,
)
from ..widgets import (
    IlluminaClipOptionWidget,
    SlidingWindowOptionWidget,
)


class OptionsPage(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)
        self.load_stylesheet(QGuiApplication.styleHints().colorScheme())
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)

    def setup_ui(self):
        self.setObjectName("OptionsPageWidget")

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(40)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

        # main container

        self.main_container_widget = QWidget(self)
        self.main_container_widget.setObjectName("MainContainerWidget")
        self.main_layout.addWidget(self.main_container_widget, 2)

        self.main_container_layout = QVBoxLayout(self.main_container_widget)
        self.main_container_layout.setContentsMargins(0, 0, 0, 0)
        self.main_container_layout.setSpacing(20)
        self.main_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_container_widget.setLayout(self.main_container_layout)

        # options container widget

        self.options_container_widget = QWidget(self)
        self.options_container_widget.setObjectName("OptionsPageWidgetContainer")
        self.options_container_widget.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.main_container_layout.addWidget(self.options_container_widget)

        self.container_layout = QGridLayout(self.options_container_widget)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(20)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.options_container_widget.setLayout(self.container_layout)

        # options column 0

        self.threads_selector_widget = ThreadsSelectorWidget(self)
        self.container_layout.addWidget(self.threads_selector_widget, 0, 0, 1, 1)

        self.illumina_clip_option_widget = IlluminaClipOptionWidget(self)
        self.container_layout.addWidget(self.illumina_clip_option_widget, 1, 0, 7, 1)

        # options column 1

        self.quality_scores_format_options_widget = SegmentedOptionWidget(
            "Quality Scores Format",
            ["Phred33", "Phred64"],
            self,
        )
        self.container_layout.addWidget(
            self.quality_scores_format_options_widget, 0, 1, 1, 1
        )

        self.sliding_window_option_widget = SlidingWindowOptionWidget(self)
        self.container_layout.addWidget(self.sliding_window_option_widget, 1, 1, 3, 1)

        self.leading_option_widget = NumberSelectorOptionWidget("Leading", self)
        self.container_layout.addWidget(self.leading_option_widget, 4, 1, 2, 1)

        self.trailing_option_widget = NumberSelectorOptionWidget("Trailing", self)
        self.container_layout.addWidget(self.trailing_option_widget, 6, 1, 2, 1)

        # options column 2

        self.minlen_option_widget = NumberSelectorOptionWidget("Minlen", self)
        self.container_layout.addWidget(self.minlen_option_widget, 0, 2, 2, 1)

        self.crop_option_widget = NumberSelectorOptionWidget("Crop", self)
        self.container_layout.addWidget(self.crop_option_widget, 2, 2, 2, 1)

        self.headcrop_option_widget = NumberSelectorOptionWidget("Headcrop", self)
        self.container_layout.addWidget(self.headcrop_option_widget, 4, 2, 2, 1)

        # navigation buttons

        self.navigation_buttons_widget = QWidget(self)
        self.navigation_buttons_widget.setObjectName("NavigationButtonsWidget")
        self.navigation_buttons_widget.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.main_container_layout.addWidget(
            self.navigation_buttons_widget, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.navigation_buttons_layout = QHBoxLayout(self.navigation_buttons_widget)
        self.navigation_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.navigation_buttons_layout.setSpacing(20)
        self.navigation_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.navigation_buttons_widget.setLayout(self.navigation_buttons_layout)

        self.back_button = QPushButton("Atrás", self.navigation_buttons_widget)
        self.back_button.setObjectName("NavigationButton")
        self.back_button.setMinimumWidth(200)
        self.back_button.setMinimumHeight(50)
        self.navigation_buttons_layout.addWidget(
            self.back_button, alignment=Qt.AlignmentFlag.AlignLeft
        )

        self.trimmer_button = QPushButton("Recortar", self.navigation_buttons_widget)
        self.trimmer_button.setObjectName("ExecuteButton")
        self.trimmer_button.setMinimumWidth(200)
        self.trimmer_button.setMinimumHeight(50)
        self.navigation_buttons_layout.addWidget(
            self.trimmer_button, alignment=Qt.AlignmentFlag.AlignRight
        )

        # saved configurations container widget

        self.saved_configurations_widget = QWidget(self)
        self.saved_configurations_widget.setObjectName("SavedConfigurationsWidget")
        self.saved_configurations_widget.setVisible(False)  # Initially hidden
        self.main_layout.addWidget(self.saved_configurations_widget, 1)

        self.saved_configurations_layout = QVBoxLayout(self.saved_configurations_widget)
        self.saved_configurations_layout.setContentsMargins(0, 0, 0, 0)
        self.saved_configurations_layout.setSpacing(20)
        self.saved_configurations_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.saved_configurations_widget.setLayout(self.saved_configurations_layout)

        self.saved_configurations_label = QLabel(
            "Configuraciones guardadas", self.saved_configurations_widget
        )
        self.saved_configurations_label.setObjectName("SavedConfigurationsLabel")
        self.saved_configurations_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.saved_configurations_layout.addWidget(self.saved_configurations_label)

        self.list_widget = ListWidget(self.saved_configurations_widget)
        self.saved_configurations_layout.addWidget(self.list_widget)

    def uncheck_include_sq_tags(self, checked: bool):
        if not checked:
            self.include_sq_tags.set_checked(False)

    def disable_min_lis(self, checked: bool):
        if checked:
            self.min_lis.checkbox.setChecked(False)

    def disable_num_alignments(self, checked: bool):
        if checked:
            self.num_alignments.checkbox.setChecked(False)

    def disable_no_best(self, checked: bool):
        if checked:
            self.no_best.checkbox.setChecked(False)

    def load_stylesheet(self, scheme: Qt.ColorScheme):
        qss_file = QFile(
            f":/styles/{Path(__file__).stem}_{"dark" if scheme == Qt.ColorScheme.Dark else "light"}.qss"
        )
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            style = self.style()
            style.unpolish(self)
            style.polish(self)
            self.update()
            qss_file.close()

    def paintEvent(self, _):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
