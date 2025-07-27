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

        # options column 0

        self.threads_selector_widget = ThreadsSelectorWidget(self)
        self.threads_selector_widget.help.setToolTip(
            "Número de subprocesos (CPU cores) que se usarán para procesar en paralelo, acelerando el recorte de las lecturas."
        )
        self.container_layout.addWidget(self.threads_selector_widget, 0, 0, 1, 1)

        self.illumina_clip_option_widget = IlluminaClipOptionWidget(self)
        self.illumina_clip_option_widget.help_button.setToolTip(
            """
            Elimina adaptadores tipo Illumina usando detección palindrómica y simple.
                • Adaptador: Archivo FASTA con la(s) secuencia(s) de adaptador que Trimmomatic debe buscar y recortar.
                • Seed Mismatches: Nº máximo de desacuerdos permitidos cuando se alinea la “semilla” inicial del adaptador.
                • Palindrome Clip Threshold: Umbral de puntaje mínimo para recortar adaptadores palindrómicos (útil en PE para detectar adaptadores inversos).
                • Simple Clip Threshold: Umbral de puntaje mínimo para recorte de adaptadores en modo “simple” (alineación directa).
                • Minimum Adapter Length: Longitud mínima de la porción alineada al adaptador para que el recorte se lleve a cabo.
                • Keep Both Reads: (PE) Conserva ambos extremos del par aunque sólo uno contenga adaptador; por defecto sólo se devuelve el extremo “limpio”.
            """
        )
        self.container_layout.addWidget(self.illumina_clip_option_widget, 1, 0, 7, 1)

        # options column 1

        self.quality_scores_format_options_widget = SegmentedOptionWidget(
            "Quality Scores Format",
            ["Phred33", "Phred64"],
            self,
        )
        self.quality_scores_format_options_widget.help_button.setToolTip(
            "Define la codificación de calidad de las bases: Phred33 (0-41) o Phred64 (0-62)."
        )
        self.container_layout.addWidget(
            self.quality_scores_format_options_widget, 0, 1, 1, 1
        )

        self.sliding_window_option_widget = SlidingWindowOptionWidget(self)
        self.sliding_window_option_widget.help_button.setToolTip(
            """
            Recorta regiones de baja calidad analizando ventanas móviles a lo largo de cada lectura.
                • Window Size: Tamaño (en nucleótidos) de la ventana que se desplaza por la lectura.
                • Quality Threshold: Calidad media mínima requerida dentro de cada ventana; si baja de este valor, se recortan las bases restantes.
            """
        )
        self.container_layout.addWidget(self.sliding_window_option_widget, 1, 1, 3, 1)

        self.leading_option_widget = NumberSelectorOptionWidget("Leading", self)
        self.leading_option_widget.help_button.setToolTip(
            "Recorta desde el extremo 5' de la lectura todas las bases cuya calidad sea inferior al umbral especificado."
        )
        self.container_layout.addWidget(self.leading_option_widget, 4, 1, 2, 1)

        self.trailing_option_widget = NumberSelectorOptionWidget("Trailing", self)
        self.trailing_option_widget.help_button.setToolTip(
            "Recorta desde el extremo 3' de la lectura todas las bases cuya calidad sea inferior al umbral especificado."
        )
        self.container_layout.addWidget(self.trailing_option_widget, 6, 1, 2, 1)

        # options column 2

        self.minlen_option_widget = NumberSelectorOptionWidget("Minlen", self)
        self.minlen_option_widget.help_button.setToolTip(
            "Longitud mínima que debe tener la lectura tras todos los recortes; si es más corta, se descarta por completo."
        )
        self.container_layout.addWidget(self.minlen_option_widget, 0, 2, 2, 1)

        self.crop_option_widget = NumberSelectorOptionWidget("Crop", self)
        self.crop_option_widget.help_button.setToolTip(
            "Recorta cada lectura a la longitud fija indicada, eliminando cualquier base que exceda ese punto."
        )
        self.container_layout.addWidget(self.crop_option_widget, 2, 2, 2, 1)

        self.headcrop_option_widget = NumberSelectorOptionWidget("Headcrop", self)
        self.headcrop_option_widget.help_button.setToolTip(
            "Elimina un número fijo de nucleótidos desde el extremo 5' de la lectura antes de aplicar cualquier otro recorte."
        )
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
