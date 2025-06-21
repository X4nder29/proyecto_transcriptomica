from pathlib import Path
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QStyleOption,
    QStyle,
    QSizePolicy,
    QTextEdit,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QFile, QTextStream, QEvent


class CliDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_stylesheet()

    def setup_ui(self):
        self.setObjectName("CliDialog")
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
        )
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumWidth(500)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        self.setLayout(self.main_layout)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.text_edit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.main_layout.addWidget(self.text_edit)

    def set_command(self, command: str):
        """Set the command to be displayed in the dialog."""
        self.text_edit.setPlainText(command)

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

    def event(self, event):
        # Se dispara cuando la ventana pierde activación (clic fuera)
        if event.type() == QEvent.WindowDeactivate:
            self.close()
            return True
        return super().event(event)
