from pathlib import Path
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QLabel, QProgressBar, QPushButton
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, QFile, QTextStream


class ReportGenerationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_stylesheet(QGuiApplication.styleHints().colorScheme())
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)

    def setup_ui(self):
        self.setObjectName("ReportGenerationWidget")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

        self.main_layout.addStretch()

        self.container = QWidget(self)
        self.container.setObjectName("ReportGenerationContainer")
        self.main_layout.addWidget(self.container)

        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(20, 20, 20, 20)
        self.container_layout.setSpacing(5)
        self.container.setLayout(self.container_layout)

        self.label = QLabel(self.container)
        self.label.setObjectName("ReportGenerationLabel")
        self.label.setText("Generating report, please wait...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.container_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.progress_bar = QProgressBar(self.container)
        self.progress_bar.setObjectName("ReportGenerationProgressBar")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.container_layout.addWidget(self.progress_bar, alignment=Qt.AlignmentFlag.AlignCenter)

        self.cancel_button = QPushButton(self.container)
        self.cancel_button.setObjectName("ReportGenerationCancelButton")
        self.cancel_button.setText("Cancel")
        self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.container_layout.addWidget(self.cancel_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addStretch()

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
