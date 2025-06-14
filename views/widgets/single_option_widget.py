from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QStyleOption,
    QStyle,
    QLabel,
    QPushButton,
)
from PySide6.QtGui import QPainter, QIcon
from PySide6.QtCore import Qt, QFile, QTextStream


class SingleOptionWidget(QWidget):

    def __init__(self, label: str, parent=None):
        super().__init__(parent)

        self.label = label

        self.setObjectName("SingleOptionWidget")
        self.setMinimumWidth(300)

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.checkbox = QPushButton(self)
        self.checkbox.setObjectName("Checkbox")
        self.checkbox.setCheckable(True)
        self.checkbox.setChecked(False)
        self.checkbox.setIcon(QIcon(":/assets/checkbox_outlined.svg"))
        self.checkbox.toggled.connect(self.toggle_checkbox_icon)
        self.main_layout.addWidget(self.checkbox, alignment=Qt.AlignmentFlag.AlignLeft)

        self.name_label = QLabel(self.label, self)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(
            self.name_label, alignment=Qt.AlignmentFlag.AlignVCenter
        )

        self.main_layout.addStretch()

        self.help_button = QPushButton("?", self)
        self.help_button.setObjectName("HelpButton")
        self.help_button.setToolTip("Help")
        self.main_layout.addWidget(
            self.help_button, alignment=Qt.AlignmentFlag.AlignRight
        )

    def toggle_checkbox_icon(self):
        if self.checkbox.isChecked():
            self.checkbox.setIcon(QIcon(":/assets/checkbox_filled.svg"))
        else:
            self.checkbox.setIcon(QIcon(":/assets/checkbox_outlined.svg"))

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
