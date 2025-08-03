from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, QFile, QTextStream
from .checkbox_widget import CheckBoxWidget


class CheckBoxSuboptionWidget(QWidget):
    def __init__(self, title: str, parent=None, checked: bool = False):
        super().__init__(parent)
        self.title = title
        self.checked = checked
        self.load_stylesheet(QGuiApplication.styleHints().colorScheme())
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)

    def setup_ui(self):
        self.setObjectName("CheckBoxSuboptionWidget")
        self.setMinimumWidth(300)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        self.checkbox = CheckBoxWidget(self, checked=self.checked)
        self.main_layout.addWidget(self.checkbox, alignment=Qt.AlignmentFlag.AlignLeft)

        # label
        self.label = QLabel(self.title, self)
        self.label.setObjectName("SubOptionWidgetLabel")
        self.label.setToolTip("Enable or disable this option")
        self.main_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft)

        # spacer
        self.main_layout.addStretch(1)

    def checked(self) -> bool:
        """Returns the checked state of the checkbox."""
        return self.checkbox.isChecked()

    def set_checked(self, checked: bool):
        """Sets the checked state of the checkbox."""
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
