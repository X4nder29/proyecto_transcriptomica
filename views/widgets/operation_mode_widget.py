from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSizePolicy,
    QStyleOption,
    QStyle,
    QButtonGroup,
    QPushButton,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import QFile, QTextStream


class OperationModeWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("OperationModeWidget")

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        self.setLayout(self.main_layout)

        self.button_group = QButtonGroup(self)
        self.button_group.setObjectName("OperationModeButtonGroup")

        self.single_end_button = QPushButton("Single End", self)
        self.single_end_button.setCheckable(True)
        self.single_end_button.setObjectName("ModeButton")
        self.single_end_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.single_end_button.setChecked(True)
        self.button_group.addButton(self.single_end_button)
        self.main_layout.addWidget(self.single_end_button)

        self.paired_end_button = QPushButton("Paired End", self)
        self.paired_end_button.setCheckable(True)
        self.paired_end_button.setObjectName("ModeButton")
        self.paired_end_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.button_group.addButton(self.paired_end_button)
        self.main_layout.addWidget(self.paired_end_button)

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
