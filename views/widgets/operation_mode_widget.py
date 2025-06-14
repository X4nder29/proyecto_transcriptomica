from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QButtonGroup,
    QStyle,
    QStyleOption,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QFile, QTextStream


class OperationModeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("OperationModeWidget")
        self.setMinimumWidth(300)

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.head = QWidget(self)
        self.head.setObjectName("Head")
        self.main_layout.addWidget(self.head)

        self.head_layout = QHBoxLayout(self.head)
        self.head_layout.setContentsMargins(0, 0, 0, 0)
        self.head_layout.setSpacing(10)
        self.head.setLayout(self.head_layout)

        self.name = QLabel("Operation Mode", self.head)
        self.name.setObjectName("OperationModeLabel")
        self.head_layout.addWidget(self.name, alignment=Qt.AlignmentFlag.AlignLeft)

        self.help_button = QPushButton("?", self.head)
        self.help_button.setObjectName("HelpButton")
        self.help_button.setToolTip("Help")
        self.head_layout.addWidget(self.help_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.body = QWidget(self)
        self.body.setObjectName("Body")
        self.main_layout.addWidget(self.body)

        self.body_layout = QHBoxLayout(self.body)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(10)
        self.body.setLayout(self.body_layout)

        self.button_group = QButtonGroup(self.body)
        self.button_group.setObjectName("OperationModeButtonGroup")
        self.button_group.setExclusive(True)
        self.button_group.setId(self.help_button, 0)

        self.simple_end_button = QPushButton("Simple End", self.body)
        self.simple_end_button.setObjectName("ModeButton")
        self.simple_end_button.setCheckable(True)
        self.simple_end_button.setToolTip("Simple End Mode")
        self.button_group.addButton(self.simple_end_button, 1)
        self.simple_end_button.setChecked(True)
        self.body_layout.addWidget(self.simple_end_button)

        self.paired_end_button = QPushButton("Paired End", self.body)
        self.paired_end_button.setObjectName("ModeButton")
        self.paired_end_button.setCheckable(True)
        self.paired_end_button.setToolTip("Paired End Mode")
        self.button_group.addButton(self.paired_end_button, 2)
        self.body_layout.addWidget(self.paired_end_button)

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
