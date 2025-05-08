from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStyleOption,
    QStyle
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from pathlib import Path


class ConfigWidget(QWidget):

    def __init__(self, name: str, parent=None):
        super().__init__(parent)

        self.name = name

        self.setObjectName("ConfigWidget")

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        self.setLayout(self.main_layout)

        self.name = QLabel(self.name)
        self.main_layout.addWidget(self.name, alignment=Qt.AlignmentFlag.AlignLeft)

        self.main_layout.addStretch()

        self.load_button = QPushButton("Cargar")
        self.main_layout.addWidget(self.load_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.delete_button = QPushButton("Eliminar")
        self.main_layout.addWidget(self.delete_button, alignment=Qt.AlignmentFlag.AlignRight)

    def load_stylesheet(self):
        styles_path = Path(__file__).parent / "config_widget.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
        super().paintEvent(event)
