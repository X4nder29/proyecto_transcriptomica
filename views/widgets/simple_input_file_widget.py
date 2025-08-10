from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStyleOption,
    QStyle,
)
from PySide6.QtGui import QGuiApplication, QPainter
from PySide6.QtCore import Qt, QFile, QTextStream
from views.widgets import SelectFilePushButton


class SimpleInputFileWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.load_stylesheet(QGuiApplication.styleHints().colorScheme())
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)

    def setup_ui(self):
        self.setObjectName("InputFileWidget")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        self.setLayout(self.main_layout)

        self.head_widget = QWidget(self)
        self.head_widget.setObjectName("HeadWidget")
        self.main_layout.addWidget(self.head_widget, alignment=Qt.AlignmentFlag.AlignTop)

        self.head_widget_layout = QHBoxLayout(self.head_widget)
        self.head_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.head_widget_layout.setSpacing(0)
        self.head_widget.setLayout(self.head_widget_layout)

        self.title_label = QLabel(self.head_widget)
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setText("Archivo de entrada")
        self.head_widget_layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.select_file_button = SelectFilePushButton(self)
        self.main_layout.addWidget(self.select_file_button)

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
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
        super().paintEvent(_)
