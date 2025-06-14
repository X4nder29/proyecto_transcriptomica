from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QLabel,
    QStyle,
    QStyleOption,
)
from PySide6.QtCore import Qt, QFile, QTextStream
from PySide6.QtGui import QPainter
from pathlib import Path
from .....widgets import InfoRow


class BasicStatistics(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("BasicStatistics")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        self.title = QLabel("Basic Statistics", self)
        self.title.setObjectName("BasicStatisticsTitle")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignTop)

        # File Type Info
        self.file_type_info = InfoRow("File Type", "FASTQ", self)
        self.file_type_info.setObjectName("FileTypeInfo")
        self.main_layout.addWidget(self.file_type_info, alignment=Qt.AlignmentFlag.AlignTop)

        # Encoding Info

        self.encoding_info = InfoRow("Encoding", "Sanger", self)
        self.encoding_info.setObjectName("EncodingInfo")
        self.main_layout.addWidget(self.encoding_info, alignment=Qt.AlignmentFlag.AlignTop)

        # Total Sequences Info
        self.total_sequences_info = InfoRow("Total Sequences", "1000000", self)
        self.total_sequences_info.setObjectName("TotalSequencesInfo")
        self.main_layout.addWidget(self.total_sequences_info, alignment=Qt.AlignmentFlag.AlignTop)

        # Sequence Flagged as Poor Quality Info
        self.poor_quality_info = InfoRow("Sequences Flagged as Poor Quality", "0", self)
        self.poor_quality_info.setObjectName("PoorQualityInfo")
        self.main_layout.addWidget(self.poor_quality_info, alignment=Qt.AlignmentFlag.AlignTop)

        # Sequence Length Info
        self.sequence_length_info = InfoRow("Sequence Length", "75", self)
        self.sequence_length_info.setObjectName("SequenceLengthInfo")
        self.main_layout.addWidget(self.sequence_length_info, alignment=Qt.AlignmentFlag.AlignTop)

        # %GC Content Info
        self.gc_content_info = InfoRow("%GC Content", "50.0", self)
        self.gc_content_info.setObjectName("GCContentInfo")
        self.main_layout.addWidget(self.gc_content_info, alignment=Qt.AlignmentFlag.AlignTop)

        # body widgets setup can be added here

        self.setLayout(self.main_layout)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
