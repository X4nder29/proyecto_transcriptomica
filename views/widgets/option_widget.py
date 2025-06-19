from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStyleOption,
    QStyle,
    QLabel,
    QPushButton,
)
from PySide6.QtGui import QIcon, QPainter
from PySide6.QtCore import Qt, QFile, QTextStream


class OptionWidget(QWidget):
    def __init__(
        self, parent: QWidget = None, title: str = None, checkable: bool = True, checked: bool = False
    ):
        super().__init__(parent)
        self.title = title
        self.checkable = checkable
        self.checked = checked
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("OptionWidget")
        self.setMinimumWidth(300)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # head
        self.head = QWidget(self)
        self.head.setObjectName("OptionWidgetHeader")
        self.main_layout.addWidget(self.head)

        self.head_layout = QHBoxLayout(self.head)
        self.head_layout.setContentsMargins(0, 0, 0, 0)
        self.head_layout.setSpacing(10)
        self.head.setLayout(self.head_layout)

        if self.checkable:
            self.checkbox = QPushButton(self)
            self.checkbox.setObjectName("OptionWidgetCheckbox")
            self.checkbox.setCheckable(True)
            self.checkbox.setChecked(self.checked)
            self.checkbox.setIcon(QIcon(":/assets/checkbox_outlined.svg"))
            self.checkbox.toggled.connect(self._toggle_checkbox_icon)
            self.head_layout.addWidget(
                self.checkbox, alignment=Qt.AlignmentFlag.AlignLeft
            )

        if self.title:
            self.label = QLabel(self.title, self)
            self.label.setObjectName("OptionWidgetLabel")
            self.label.setToolTip("Enable or disable this option")
            self.head_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.head_layout.addStretch(1)

        self.help_button = QPushButton("?", self)
        self.help_button.setObjectName("OptionWidgetHelpPushButton")
        self.help_button.setToolTip("Help")
        self.head_layout.addWidget(
            self.help_button, alignment=Qt.AlignmentFlag.AlignRight
        )

    def _toggle_checkbox_icon(self):
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

    def paintEvent(self, _):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
        super().paintEvent(_)
