from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QStyleOption,
    QStyle,
    QPushButton,
)
from PySide6.QtGui import QGuiApplication, QPainter, QIcon
from PySide6.QtCore import Qt, QFile, QTextStream


class CheckBoxWidget(QPushButton):
    def __init__(self, parent: QWidget = None, checked: bool = False):
        super().__init__(parent)
        self.checked = checked
        self.load_stylesheet(QGuiApplication.styleHints().colorScheme())
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)

    def setup_ui(self):
        self.setObjectName("CheckBoxWidget")
        self.setCheckable(True)
        self.setChecked(self.checked)
        self.setIcon(QIcon(":/assets/checkbox_outlined.svg"))
        self.toggled.connect(self._toggle_checkbox_icon)

    def _toggle_checkbox_icon(self):
        if self.isChecked():
            self.setIcon(QIcon(":/assets/checkbox_filled.svg"))
        else:
            self.setIcon(QIcon(":/assets/checkbox_outlined.svg"))

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
