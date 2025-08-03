from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QSizePolicy,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, QFile, QTextStream
from .decimal_selector import DecimalSelector
from .checkbox_widget import CheckBoxWidget


class DecimalSelectorSuboptionWidget(QWidget):
    def __init__(
        self,
        title: str,
        parent: QWidget = None,
        checkable: bool = False,
        checked: bool = False,
        decimals: int = 1,
        step: float = 0.1,
    ):
        super().__init__(parent)

        self.title = title
        self.checkable = checkable
        self.checked = checked
        self.decimals = decimals
        self.step = step

        self.load_stylesheet(QGuiApplication.styleHints().colorScheme())
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)

    def setup_ui(self):
        self.setObjectName("SubOptionWidget")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        # checkbox
        if self.checkable:
            self.check_box_widget = CheckBoxWidget(self)
            self.check_box_widget.clicked.connect(self.toggle_suboption)
            self.main_layout.addWidget(
                self.check_box_widget, alignment=Qt.AlignmentFlag.AlignLeft
            )

        # label
        self.label = QLabel(self.title, self)
        self.label.setObjectName("SubOptionWidgetLabel")
        self.label.setToolTip("Enable or disable this option")
        self.main_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft)

        # spacer
        self.main_layout.addStretch(1)

        # number selector
        self.decimal_selector = DecimalSelector(
            self, decimals=self.decimals, step=self.step
        )
        self.decimal_selector.setEnabled(self.checked if self.checkable else True)
        self.main_layout.addWidget(
            self.decimal_selector, alignment=Qt.AlignmentFlag.AlignRight
        )

    def toggle_suboption(self, checked: bool):
        self.decimal_selector.setEnabled(checked)

    def value(self):
        return self.decimal_selector.value()

    def set_value(self, value: float):
        self.decimal_selector.set_value(value)

    def set_decimals(self, decimals: int):
        self.decimal_selector.set_decimals(decimals)

    def set_range(self, minimum: float, maximum: float):
        self.decimal_selector.set_range(minimum, maximum)

    def set_single_step(self, step: float):
        self.decimal_selector.set_single_step(step)

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
