from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QStyleOption,
    QStyle,
    QSizePolicy,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QFile, QTextStream
from .number_selector import NumberSelector
from .checkbox_widget import CheckBoxWidget


class NumberSelectorSuboptionWidget(QWidget):
    def __init__(self, title: str, parent: QWidget = None, checkable: bool = False, checked: bool = False):
        super().__init__(parent)

        self.title = title
        self.checkable = checkable
        self.checked = checked

        self.setObjectName("SubOptionWidget")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
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
        self.number_selector = NumberSelector(self)
        self.number_selector.setEnabled(self.checked if self.checkable else True)
        self.main_layout.addWidget(
            self.number_selector, alignment=Qt.AlignmentFlag.AlignRight
        )

    def toggle_suboption(self, checked: bool):
        self.number_selector.setEnabled(checked)

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
