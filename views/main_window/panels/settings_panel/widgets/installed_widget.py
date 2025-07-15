from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QStyleOption,
    QStyle,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtGui import QPainter, QIcon
from PySide6.QtCore import Qt, QFile, QTextStream


class InstalledWidget(QWidget):

    def __init__(self, title: str, parent: QWidget = None, installed: bool = False):
        super().__init__(parent=parent)
        self.title = title
        self.installed = installed
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        """Setup the UI for the Installed Widget."""
        self.setObjectName("InstalledWidget")

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        self.setLayout(self.main_layout)

        self.title_label = QLabel(self.title, self)
        self.title_label.setObjectName("TitleLabel")
        self.main_layout.addWidget(
            self.title_label, alignment=Qt.AlignmentFlag.AlignLeft
        )

        self.installed_push_button = QPushButton(self)
        self.installed_push_button.setObjectName("InstalledPushButton")
        self.installed_push_button.setIcon(
            QIcon(":/assets/install_filled.svg")
            if self.installed
            else QIcon(":/assets/install_outlined.svg")
        )
        self.main_layout.addWidget(
            self.installed_push_button, alignment=Qt.AlignmentFlag.AlignRight
        )

    def set_installed(self, installed: bool):
        """Set the installed state of the widget."""
        self.installed = installed
        self.installed_push_button.setIcon(
            QIcon(":/assets/install_filled.svg")
            if self.installed
            else QIcon(":/assets/install_outlined.svg")
        )
        self.installed_push_button.setEnabled(not self.installed)

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
