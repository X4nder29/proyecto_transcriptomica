from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QStyleOption,
    QStyle,
    QSizePolicy,
    QLabel,
    QProgressBar,
    QPushButton,
)
from PySide6.QtGui import QPainter, QFontMetrics
from PySide6.QtCore import Qt, QFile, QTextStream


class GenerationPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("GenerationPageWidget")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

        self.progress_bar_widget = QWidget(self)
        self.progress_bar_widget.setObjectName("ProgressBarWidget")
        self.main_layout.addWidget(
            self.progress_bar_widget, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.progress_bar_layout = QVBoxLayout(self.progress_bar_widget)
        self.progress_bar_layout.setContentsMargins(40, 20, 40, 20)
        self.progress_bar_layout.setSpacing(5)
        self.progress_bar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar_widget.setLayout(self.progress_bar_layout)

        self.title_label = QLabel("Generation Progress", self)
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar_layout.addWidget(
            self.title_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setObjectName("GenerationProgressBar")
        self.progress_bar.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar_layout.addWidget(
            self.progress_bar, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setObjectName("CancelButton")
        self.progress_bar_layout.addWidget(
            self.cancel_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

    def set_text(self, text: str):
        self.title_label.setText(
            QFontMetrics(self.title_label.font()).elidedText(
                text, Qt.TextElideMode.ElideRight, 300
            )
        )

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
