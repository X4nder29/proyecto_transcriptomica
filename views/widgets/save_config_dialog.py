from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QDialog,
    QVBoxLayout,
    QStyleOption,
    QStyle,
    QDialogButtonBox,
    QLineEdit,
)
from PySide6.QtGui import QGuiApplication, QPainter
from PySide6.QtCore import Qt, QFile, QTextStream


class SaveConfigDialog(QDialog):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.load_stylesheet(QGuiApplication.styleHints().colorScheme())
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)

    def setup_ui(self):
        self.setWindowTitle("Save Configuration")
        self.setObjectName("SaveConfigDialog")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        self.config_name = QLineEdit(self)
        self.config_name.setObjectName("ConfigName")
        self.config_name.setPlaceholderText("Enter configuration name")
        self.config_name.setToolTip("Enter a name for the configuration")
        self.config_name.setMaxLength(50)
        self.config_name.setClearButtonEnabled(True)
        self.config_name.setMinimumWidth(300)
        self.config_name.textChanged.connect(
            lambda text: self.buttons.button(QDialogButtonBox.Ok).setEnabled(bool(text))
        )
        self.config_name.setClearButtonEnabled(True)
        self.config_name.setFocus()
        self.main_layout.addWidget(self.config_name)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self
        )
        self.buttons.setObjectName("Buttons")
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(False)

        self.main_layout.addWidget(self.buttons)

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
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
        super().paintEvent(event)
