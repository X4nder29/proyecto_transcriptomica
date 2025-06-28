from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStyleOption,
    QStyle,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QFile, QTextStream


class ConfigItemWidget(QWidget):

    def __init__(self, name: str, parent: QWidget = None):
        super().__init__(parent)
        self.name = name
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("ConfigItemWidget")

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        self.setLayout(self.main_layout)

        self.name = QLabel(self.name)
        self.main_layout.addWidget(self.name, alignment=Qt.AlignmentFlag.AlignLeft)

        self.main_layout.addStretch()

        self.load_button = QPushButton("Cargar")
        self.main_layout.addWidget(
            self.load_button, alignment=Qt.AlignmentFlag.AlignRight
        )

        self.delete_button = QPushButton("Eliminar")
        self.main_layout.addWidget(
            self.delete_button, alignment=Qt.AlignmentFlag.AlignRight
        )

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
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
        super().paintEvent(event)
