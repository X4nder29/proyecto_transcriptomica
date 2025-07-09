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
        self.operation_mode_widget.help_button.setToolTip(
            "Elige si el archivo de entrada contiene lecturas single-end (una sola lectura por \nfragmento) o paired-end (dos lecturas emparejadas)."
        )
        self.main_layout.addWidget(self.operation_mode_widget, 0, 0, 1, 1)

        self.simple_input_file_widget = SimpleInputFileWidget(self)
        self.simple_input_file_widget.help_push_button.setToolTip(
            "Selecciona el archivo FASTQ de entrada. Si es single-end, se usará este archivo para el recorte."
        )
        self.main_layout.addWidget(self.simple_input_file_widget, 1, 0, 3, 1)

        self.paired_input_file_widget = PairedInputFileWidget(self)
        self.paired_input_file_widget.help_push_button.setToolTip(
            "Selecciona el archivo FASTQ de entrada para lecturas emparejadas. Si es paired-end, \nse usará este archivo junto con el anterior para el recorte."
        )
        self.paired_input_file_widget.setVisible(False)
        self.main_layout.addWidget(self.paired_input_file_widget, 1, 0, 5, 1)

        self.threads_selector_widget = ThreadsSelectorWidget(self)
        self.threads_selector_widget.help.setToolTip(
            "Número de subprocesos (CPU cores) que se usarán para procesar en paralelo, acelerando el recorte de las lecturas."
        )
        self.main_layout.addWidget(self.threads_selector_widget, 0, 1, 1, 1)

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
        self.main_layout.addWidget(self.illumina_clip_option_widget, 1, 1, 7, 1)

        self.sliding_window_option_widget = SlidingWindowOptionWidget(self)
        self.sliding_window_option_widget.help_button.setToolTip(
            """
            Recorta regiones de baja calidad analizando ventanas móviles a lo largo de cada lectura.
                • Window Size: Tamaño (en nucleótidos) de la ventana que se desplaza por la lectura.
                • Quality Threshold: Calidad media mínima requerida dentro de cada ventana; si baja de este valor, se recortan las bases restantes.
            """
        )
        self.main_layout.addWidget(self.sliding_window_option_widget, 8, 1, 3, 1)

        self.quality_scores_format_options_widget = SegmentedOptionWidget(
            "Quality Scores Format",
            ["Phred33", "Phred64"],
            self,
        )
        self.quality_scores_format_options_widget.help_button.setToolTip(
            "Define la codificación de calidad de las bases: Phred33 (0-41) o Phred64 (0-62)."
        )
        self.main_layout.addWidget(
            self.quality_scores_format_options_widget, 0, 2, 1, 1
        )

        self.leading_option_widget = NumberSelectorOptionWidget("Leading", self)
        self.leading_option_widget.help_button.setToolTip(
            "Recorta desde el extremo 5' de la lectura todas las bases cuya calidad sea inferior al umbral especificado."
        )
        self.main_layout.addWidget(self.leading_option_widget, 1, 2, 2, 1)

        self.trailing_option_widget = NumberSelectorOptionWidget("Trailing", self)
        self.trailing_option_widget.help_button.setToolTip(
            "Recorta desde el extremo 3' de la lectura todas las bases cuya calidad sea inferior al umbral especificado."
        )
        self.main_layout.addWidget(self.trailing_option_widget, 3, 2, 2, 1)

        self.minlen_option_widget = NumberSelectorOptionWidget("Minlen", self)
        self.minlen_option_widget.help_button.setToolTip(
            "Longitud mínima que debe tener la lectura tras todos los recortes; si es más corta, se descarta por completo."
        )
        self.main_layout.addWidget(self.minlen_option_widget, 5, 2, 2, 1)

        self.crop_option_widget = NumberSelectorOptionWidget("Crop", self)
        self.crop_option_widget.help_button.setToolTip(
            "Recorta cada lectura a la longitud fija indicada, eliminando cualquier base que exceda ese punto."
        )
        self.main_layout.addWidget(self.crop_option_widget, 7, 2, 2, 1)

        self.headcrop_option_widget = NumberSelectorOptionWidget("Headcrop", self)
        self.headcrop_option_widget.help_button.setToolTip(
            "Elimina un número fijo de nucleótidos desde el extremo 5' de la lectura antes de aplicar cualquier otro recorte."
        )
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
