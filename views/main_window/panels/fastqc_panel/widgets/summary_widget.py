from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QLabel,
    QButtonGroup,
    QPushButton,
)
from PySide6.QtCore import Qt, QFile, QTextStream


class SummaryListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("SummaryListWidget")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumWidth(300)

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)
        self.setLayout(self.main_layout)

        self.head_widget = QWidget(self)
        self.head_widget.setObjectName("SummaryListWidgetHead")
        self.main_layout.addWidget(self.head_widget, alignment=Qt.AlignmentFlag.AlignTop)

        self.head_widget_layout = QHBoxLayout(self.head_widget)
        self.head_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.head_widget_layout.setSpacing(0)
        self.head_widget_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.head_widget.setLayout(self.head_widget_layout)

        self.summary_label = QLabel("Resumen", self.head_widget)
        self.summary_label.setObjectName("SummaryLabel")
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.head_widget_layout.addWidget(
            self.summary_label, alignment=Qt.AlignmentFlag.AlignLeft
        )

        self.help_button = QPushButton("?", self.head_widget)
        self.help_button.setObjectName("HelpButton")
        self.help_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.help_button.setToolTip("Ayuda")
        self.head_widget_layout.addWidget(self.help_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.button_group = QButtonGroup(self)
        self.button_group.setObjectName("SummaryButtonGroup")
        self.button_group.setExclusive(True)

        self.per_base_sequence_quality_push_button = QPushButton(
            "Calidad de secuencia por base", self
        )
        self.per_base_sequence_quality_push_button.setObjectName("SummaryItem")
        self.per_base_sequence_quality_push_button.setCheckable(True)
        self.per_base_sequence_quality_push_button.setEnabled(False)
        self.button_group.addButton(self.per_base_sequence_quality_push_button)
        self.main_layout.addWidget(
            self.per_base_sequence_quality_push_button,
            alignment=Qt.AlignmentFlag.AlignTop,
        )

        self.per_sequence_quality_scores_push_button = QPushButton(
            "Puntuaciones de calidad por secuencia", self
        )
        self.per_sequence_quality_scores_push_button.setObjectName("SummaryItem")
        self.per_sequence_quality_scores_push_button.setCheckable(True)
        self.per_sequence_quality_scores_push_button.setEnabled(False)
        self.button_group.addButton(self.per_sequence_quality_scores_push_button)
        self.main_layout.addWidget(
            self.per_sequence_quality_scores_push_button,
            alignment=Qt.AlignmentFlag.AlignTop,
        )

        self.per_base_sequence_content_push_button = QPushButton(
            "Contenido de secuencia por base", self
        )
        self.per_base_sequence_content_push_button.setObjectName("SummaryItem")
        self.per_base_sequence_content_push_button.setCheckable(True)
        self.per_base_sequence_content_push_button.setEnabled(False)
        self.button_group.addButton(self.per_base_sequence_content_push_button)
        self.main_layout.addWidget(
            self.per_base_sequence_content_push_button,
            alignment=Qt.AlignmentFlag.AlignTop,
        )

        self.per_sequence_gc_content_push_button = QPushButton(
            "Contenido GC por secuencia", self
        )
        self.per_sequence_gc_content_push_button.setObjectName("SummaryItem")
        self.per_sequence_gc_content_push_button.setCheckable(True)
        self.per_sequence_gc_content_push_button.setEnabled(False)
        self.button_group.addButton(self.per_sequence_gc_content_push_button)
        self.main_layout.addWidget(
            self.per_sequence_gc_content_push_button,
            alignment=Qt.AlignmentFlag.AlignTop,
        )

        self.per_base_n_content = QPushButton("Contenido N por base", self)
        self.per_base_n_content.setObjectName("SummaryItem")
        self.per_base_n_content.setCheckable(True)
        self.per_base_n_content.setEnabled(False)
        self.button_group.addButton(self.per_base_n_content)
        self.main_layout.addWidget(
            self.per_base_n_content, alignment=Qt.AlignmentFlag.AlignTop
        )

        self.sequence_length_distribution_push_button = QPushButton(
            "Distribución de longitud de secuencia", self
        )
        self.sequence_length_distribution_push_button.setObjectName("SummaryItem")
        self.sequence_length_distribution_push_button.setCheckable(True)
        self.sequence_length_distribution_push_button.setEnabled(False)
        self.button_group.addButton(self.sequence_length_distribution_push_button)
        self.main_layout.addWidget(
            self.sequence_length_distribution_push_button,
            alignment=Qt.AlignmentFlag.AlignTop,
        )

        self.sequence_duplication_levels_push_button = QPushButton(
            "Niveles de duplicación de secuencia", self
        )
        self.sequence_duplication_levels_push_button.setObjectName("SummaryItem")
        self.sequence_duplication_levels_push_button.setCheckable(True)
        self.sequence_duplication_levels_push_button.setEnabled(False)
        self.button_group.addButton(self.sequence_duplication_levels_push_button)
        self.main_layout.addWidget(
            self.sequence_duplication_levels_push_button,
            alignment=Qt.AlignmentFlag.AlignTop,
        )

        self.overrepresented_sequences_push_button = QPushButton(
            "Secuencias sobre-representadas", self
        )
        self.overrepresented_sequences_push_button.setObjectName("SummaryItem")
        self.overrepresented_sequences_push_button.setCheckable(True)
        self.overrepresented_sequences_push_button.setEnabled(False)
        self.button_group.addButton(self.overrepresented_sequences_push_button)
        self.main_layout.addWidget(
            self.overrepresented_sequences_push_button,
            alignment=Qt.AlignmentFlag.AlignTop,
        )

        self.adapter_content_push_button = QPushButton("Contenido de adaptador", self)
        self.adapter_content_push_button.setObjectName("SummaryItem")
        self.adapter_content_push_button.setCheckable(True)
        self.adapter_content_push_button.setEnabled(False)
        self.button_group.addButton(self.adapter_content_push_button)
        self.main_layout.addWidget(
            self.adapter_content_push_button, alignment=Qt.AlignmentFlag.AlignTop
        )

        self.main_layout.addStretch()

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
