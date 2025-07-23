from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QStyleOption,
    QStyle,
    QStackedWidget,
    QLabel,
    QProgressBar,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QFile, QTextStream


class LoadingWidget(QStackedWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("LoadingWidget")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # progress

        self.progress_container = QWidget(self)
        self.progress_container.setObjectName("LoadingFilesWidget")
        self.progress_container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.addWidget(self.progress_container)

        self.loading_files_layout = QVBoxLayout(self.progress_container)
        self.loading_files_layout.setContentsMargins(0, 0, 0, 0)
        self.loading_files_layout.setSpacing(20)
        self.loading_files_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_container.setLayout(self.loading_files_layout)

        self.loading_progress_bar = QProgressBar(self.progress_container)
        self.loading_progress_bar.setObjectName("LoadingProgressBar")
        self.loading_progress_bar.setRange(0, 0)
        self.loading_progress_bar.setTextVisible(False)
        self.loading_progress_bar.setVisible(False)
        self.loading_progress_bar.setFixedHeight(50)
        self.loading_progress_bar.setFixedWidth(50)
        self.loading_files_layout.addWidget(self.loading_progress_bar)

        # error

        self.error_container = QWidget(self)
        self.error_container.setObjectName("LoadingFilesWidget")
        self.error_container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.addWidget(self.error_container)

        self.error_layout = QVBoxLayout(self.error_container)
        self.error_layout.setContentsMargins(0, 0, 0, 0)
        self.error_layout.setSpacing(20)
        self.error_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_container.setLayout(self.error_layout)

        self.error_label = QLabel(
            "Error al cargar los archivos. Por favor, inténtelo de nuevo.", self
        )
        self.error_label.setObjectName("LoadingErrorLabel")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setVisible(True)
        self.error_layout.addWidget(self.error_label)

    def set_error_message(self, message: str):
        self.error_label.setText(self.error_label.text() + f"\n{message}")

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
