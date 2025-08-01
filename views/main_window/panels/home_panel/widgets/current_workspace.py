from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QStyle,
    QStyleOption,
    QSizePolicy,
)
from PySide6.QtGui import QGuiApplication, QPainter
from PySide6.QtCore import Qt, QFile, QTextStream


class CurrentWorkspace(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)
        QGuiApplication.styleHints().colorSchemeChanged.emit(
            QGuiApplication.styleHints().colorScheme()
        )

    def setup_ui(self):
        self.setObjectName("CurrentWorkspace")
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.workspace_label = QLabel(self)
        self.workspace_label.setObjectName("WorkspaceLabel")
        self.main_layout.addWidget(self.workspace_label)

        self.workspace_path = QLabel(self)
        self.workspace_path.setObjectName("WorkspacePath")
        self.main_layout.addWidget(self.workspace_path)

    def set_workspace_name(self, name: str):
        self.workspace_label.setText(name)

    def set_workspace_path(self, path: str):
        self.workspace_path.setText(path)

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
