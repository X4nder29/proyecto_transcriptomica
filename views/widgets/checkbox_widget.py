from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QStyleOption,
    QStyle,
    QPushButton,
)
from PySide6.QtGui import QPainter, QIcon
from PySide6.QtCore import QFile, QTextStream


class CheckBoxWidget(QPushButton):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("CheckBoxWidget")
        self.setCheckable(True)
        self.setChecked(False)
        self.setIcon(QIcon(":/assets/checkbox_outlined.svg"))
        self.toggled.connect(self._toggle_checkbox_icon)

    def _toggle_checkbox_icon(self):
        if self.isChecked():
            self.setIcon(QIcon(":/assets/checkbox_filled.svg"))
        else:
            self.setIcon(QIcon(":/assets/checkbox_outlined.svg"))

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
