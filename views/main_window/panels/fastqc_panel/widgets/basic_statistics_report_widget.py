from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QSizePolicy,
    QStyleOption,
    QStyle,
    QLabel,
    QProgressBar,
    QPushButton,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QFile, QTextStream


class BasicStatisticsReportWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("BasicStatisticsReportWidget")

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        self.setLayout(self.main_layout)

        # title labels

        self._filename_title_label = QLabel(self)
        self._filename_title_label.setObjectName("BasicStatisticsTitleLabel")
        self._filename_title_label.setText("File Name")
        self._filename_title_label.setWordWrap(True)
        self._filename_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self._filename_title_label, 0, 0, 1, 1)

        self._filetype_title_label = QLabel(self)
        self._filetype_title_label.setObjectName("BasicStatisticsTitleLabel")
        self._filetype_title_label.setText("File Type")
        self._filetype_title_label.setWordWrap(True)
        self._filetype_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self._filetype_title_label, 0, 1, 1, 1)

        self._encoding_title_label = QLabel(self)
        self._encoding_title_label.setObjectName("BasicStatisticsTitleLabel")
        self._encoding_title_label.setText("Encoding")
        self._encoding_title_label.setWordWrap(True)
        self._encoding_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self._encoding_title_label, 0, 2, 1, 1)

        self._total_sequences_title_label = QLabel(self)
        self._total_sequences_title_label.setObjectName("BasicStatisticsTitleLabel")
        self._total_sequences_title_label.setText("Total Sequences")
        self._total_sequences_title_label.setWordWrap(True)
        self._total_sequences_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self._total_sequences_title_label, 0, 3, 1, 1)

        self._sequences_flagged_as_poor_quiality_label = QLabel(self)
        self._sequences_flagged_as_poor_quiality_label.setObjectName(
            "BasicStatisticsTitleLabel"
        )
        self._sequences_flagged_as_poor_quiality_label.setText("Sequences Flagged as Poor Quality")
        self._sequences_flagged_as_poor_quiality_label.setWordWrap(True)
        self._sequences_flagged_as_poor_quiality_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self._sequences_flagged_as_poor_quiality_label, 0, 4, 1, 1)

        self._sequence_length_title_label = QLabel(self)
        self._sequence_length_title_label.setObjectName("BasicStatisticsTitleLabel")
        self._sequence_length_title_label.setText("Sequence Length")
        self._sequence_length_title_label.setWordWrap(True)
        self._sequence_length_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self._sequence_length_title_label, 0, 5, 1, 1)

        self._percent_gc_title_label = QLabel(self)
        self._percent_gc_title_label.setObjectName("BasicStatisticsTitleLabel")
        self._percent_gc_title_label.setText(r"%GC")
        self._percent_gc_title_label.setWordWrap(True)
        self._percent_gc_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self._percent_gc_title_label, 0, 6, 1, 1)

        # value labels

        self._filename_value_label = QLabel(self)
        self._filename_value_label.setObjectName("BasicStatisticsValueLabel")
        self._filename_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._filename_value_label.setWordWrap(True)
        self.main_layout.addWidget(self._filename_value_label, 1, 0, 1, 1)

        self._filetype_value_label = QLabel(self)
        self._filetype_value_label.setObjectName("BasicStatisticsValueLabel")
        self._filetype_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._filetype_value_label.setWordWrap(True)
        self.main_layout.addWidget(self._filetype_value_label, 1, 1, 1, 1)

        self._encoding_value_label = QLabel(self)
        self._encoding_value_label.setObjectName("BasicStatisticsValueLabel")
        self._encoding_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._encoding_value_label.setWordWrap(True)
        self.main_layout.addWidget(self._encoding_value_label, 1, 2, 1, 1)

        self._total_sequences_value_label = QLabel(self)
        self._total_sequences_value_label.setObjectName("BasicStatisticsValueLabel")
        self._total_sequences_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._total_sequences_value_label.setWordWrap(True)
        self.main_layout.addWidget(self._total_sequences_value_label, 1, 3, 1, 1)

        self._sequences_flagged_as_poor_quiality_value_label = QLabel(self)
        self._sequences_flagged_as_poor_quiality_value_label.setObjectName("BasicStatisticsValueLabel")
        self._sequences_flagged_as_poor_quiality_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._sequences_flagged_as_poor_quiality_value_label.setWordWrap(True)
        self.main_layout.addWidget(self._sequences_flagged_as_poor_quiality_value_label, 1, 4, 1, 1)

        self._sequence_length_value_label = QLabel(self)
        self._sequence_length_value_label.setObjectName("BasicStatisticsValueLabel")
        self._sequence_length_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._sequence_length_value_label.setWordWrap(True)
        self.main_layout.addWidget(self._sequence_length_value_label, 1, 5, 1, 1)

        self._percent_gc_value_label = QLabel(self)
        self._percent_gc_value_label.setObjectName("BasicStatisticsValueLabel")
        self._percent_gc_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._percent_gc_value_label.setWordWrap(True)
        self.main_layout.addWidget(self._percent_gc_value_label, 1, 6, 1, 1)

    def set_filename(self, filename: str):
        self._filename_value_label.setText(filename)

    def set_filetype(self, filetype: str):
        self._filetype_value_label.setText(filetype)

    def set_encoding(self, encoding: str):
        self._encoding_value_label.setText(encoding)

    def set_total_sequences(self, total_sequences: int):
        self._total_sequences_value_label.setText(str(total_sequences))

    def set_sequences_flagged_as_poor_quality(self, poor_quality_count: int):
        self._sequences_flagged_as_poor_quiality_value_label.setText(str(poor_quality_count))

    def set_sequence_length(self, sequence_length: str):
        self._sequence_length_value_label.setText(sequence_length)

    def set_percent_gc(self, percent_gc: str):
        self._percent_gc_value_label.setText(percent_gc)

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
