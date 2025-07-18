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
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QFile, QTextStream
from views.widgets import (
    ThreadsSelectorWidget,
    OptionWidget,
    NumberSelectorOptionWidget,
    ListWidget,
    ComboBoxOptionWidget,
)


class OptionsPage(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)
        self.load_stylesheet()
        self.setup_ui()

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

        # column 0

        self.threads_selector_widget = ThreadsSelectorWidget(self)
        self.threads_selector_widget.setObjectName("ThreadsSelectorWidget")
        self.container_layout.addWidget(self.threads_selector_widget, 0, 0, 2, 1)

        self.blast_format = ComboBoxOptionWidget(
            "Formato de salida BLAST",
            [
                ("Pairwise", "0"),
                ("Tabular", "1"),
                ("Tabular Cigar", "1 cigar"),
                ("Tabular Cigar QCoverage", "1 cigar qcov"),
                ("Tabular Cigar QCoverage Strand", "1 cigar qcov qstrand"),
            ],
            self,
        )
        self.blast_format.setObjectName("BlastFormatWidget")
        self.container_layout.addWidget(self.blast_format, 2, 0, 2, 1)

        self.num_alignments = NumberSelectorOptionWidget(
            "Número de alineamientos", self
        )
        self.num_alignments.checkbox.toggled.connect(self.disable_min_lis)
        self.container_layout.addWidget(self.num_alignments, 4, 0, 2, 1)

        # column 1

        self.min_lis = NumberSelectorOptionWidget("Longitud mínima de secuencia", self)
        self.min_lis.checkbox.toggled.connect(lambda checked: (self.disable_num_alignments(checked), self.disable_no_best(checked)))
        self.container_layout.addWidget(self.min_lis, 0, 1, 2, 1)

        self.output_no_aligned = OptionWidget(self, "Salida de Lecturas no Alineadas")
        self.container_layout.addWidget(self.output_no_aligned, 2, 1, 1, 1)

        self.output_sam = OptionWidget(self, "Archivo de alineación SAM")
        self.container_layout.addWidget(self.output_sam, 3, 1, 1, 1)

        self.include_sq_tags = OptionWidget(self, "Etiquetas adicionales SQ en SAM")
        self.include_sq_tags.setEnabled(False)
        self.container_layout.addWidget(self.include_sq_tags, 4, 1, 1, 1)
        self.output_sam.checkbox.toggled.connect(self.include_sq_tags.setEnabled)
        self.output_sam.checkbox.toggled.connect(self.uncheck_include_sq_tags)

        self.no_best = OptionWidget(self, "No mostrar el mejor alineamiento")
        self.no_best.checkbox.toggled.connect(self.disable_min_lis)
        self.container_layout.addWidget(self.no_best, 5, 1, 1, 1)

        self.paired = OptionWidget(self, "Lecturas Paired-End")
        self.paired.setEnabled(False)  # Initially disabled
        self.container_layout.addWidget(self.paired, 6, 1, 1, 1)

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

        self.filter_button = QPushButton("Filtrar", self.navigation_buttons_widget)
        self.filter_button.setObjectName("ExecuteButton")
        self.filter_button.setMinimumWidth(200)
        self.filter_button.setMinimumHeight(50)
        self.navigation_buttons_layout.addWidget(
            self.filter_button, alignment=Qt.AlignmentFlag.AlignRight
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
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
