from pathlib import Path
from typing import Tuple
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStyleOption,
    QStyle,
    QSizePolicy,
    QLabel,
    QPushButton,
    QComboBox,
)
from PySide6.QtGui import QGuiApplication, QPainter, QIcon
from PySide6.QtCore import Qt, QFile, QTextStream


class ComboBoxOptionWidget(QWidget):
    def __init__(self, label: str, options: list[Tuple[str, str]], parent: QWidget = None):
        super().__init__(parent)
        self.label = label
        self.options = options
        self.load_stylesheet(QGuiApplication.styleHints().colorScheme())
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)

    def setup_ui(self):
        self.setObjectName("ComboBoxOptionWidget")
        self.setMinimumWidth(300)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(20)

        # head

        self.head = QWidget(self)
        self.head.setObjectName("HeadWidget")
        self.main_layout.addWidget(self.head)

        self.head_layout = QHBoxLayout(self.head)
        self.head_layout.setContentsMargins(0, 0, 0, 0)
        self.head_layout.setSpacing(10)
        self.head.setLayout(self.head_layout)

        # eheckbox

        self.checkbox = QPushButton(self)
        self.checkbox.setObjectName("Checkbox")
        self.checkbox.setCheckable(True)
        self.checkbox.setChecked(False)
        self.checkbox.setIcon(QIcon(":/assets/checkbox_outlined.svg"))
        self.checkbox.toggled.connect(self.toggle_checkbox_icon)
        self.head_layout.addWidget(self.checkbox, alignment=Qt.AlignmentFlag.AlignLeft)

        # name label

        self.name_label = QLabel(self.label, self.head)
        self.name_label.setObjectName("NameLabel")
        self.head_layout.addWidget(
            self.name_label, alignment=Qt.AlignmentFlag.AlignLeft
        )

        # spacer

        self.head_layout.addStretch()

        # body

        self.body = QWidget(self)
        self.body.setObjectName("BodyWidget")
        self.main_layout.addWidget(self.body)

        self.body_layout = QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(10)
        self.body.setLayout(self.body_layout)

        # combo box

        self.combo_box = QComboBox(self.body)
        self.combo_box.setObjectName("ComboBox")
        self.combo_box.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        for option, data in self.options:
            self.combo_box.addItem(option, data)
        self.combo_box.setCurrentIndex(0)
        self.body_layout.addWidget(self.combo_box)

    def toggle_checkbox_icon(self):
        if self.checkbox.isChecked():
            self.checkbox.setIcon(QIcon(":/assets/checkbox_filled.svg"))
        else:
            self.checkbox.setIcon(QIcon(":/assets/checkbox_outlined.svg"))

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

    def paintEvent(self, event):
        option = QStyleOption()
        option.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, option, painter, self)
        super().paintEvent(event)
