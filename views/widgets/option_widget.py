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
from PySide6.QtGui import QGuiApplication, QPainter
from PySide6.QtCore import Qt, QFile, QTextStream
from .checkbox_widget import CheckBoxWidget


class OptionWidget(QWidget):
    def __init__(
        self, parent: QWidget = None, title: str = None, checkable: bool = True, checked: bool = False
    ):
        super().__init__(parent)
        self.title = title
        self.checkable = checkable
        self.checked = checked
        self.load_stylesheet(QGuiApplication.styleHints().colorScheme())
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)

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
            self.checkbox = CheckBoxWidget(self)
            self.head_layout.addWidget(
                self.checkbox, alignment=Qt.AlignmentFlag.AlignLeft
            )

        if self.title:
            self.label = QLabel(self.title, self)
            self.label.setObjectName("OptionWidgetLabel")
            self.label.setToolTip("Enable or disable this option")
            self.head_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.head_layout.addStretch(1)

    def is_checked(self):
        return self.checkbox.isChecked() if self.checkable else True

    def set_checked(self, checked: bool):
        if self.checkable:
            self.checkbox.setChecked(checked)

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
