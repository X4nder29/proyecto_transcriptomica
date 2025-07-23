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
from PySide6.QtGui import QPainter
from PySide6.QtCore import QFile, QTextStream
from .settings_item import SettingsItem


class InstalledProgramItem(QWidget):
    def __init__(self, icon, title, subtitle, parent: QWidget = None):
        super().__init__(parent)
        self.icon = icon
        self.title = title
        self.subtitle = subtitle
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("InstalledProgramItem")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(2)

        self.settings_item = SettingsItem(
            self.icon, self.title, self.subtitle, parent=self
        )
        self.main_layout.addWidget(self.settings_item)

        self.checking_indicator = QLabel("Comprobando...", self.settings_item)
        self.checking_indicator.setObjectName("CheckingIndicator")
        self.settings_item.action_layout.addWidget(self.checking_indicator)

        self.installed_indicator = QLabel("Instalado", self.settings_item)
        self.installed_indicator.setObjectName("InstalledIndicator")
        self.installed_indicator.setVisible(False)  # Initially hidden
        self.settings_item.action_layout.addWidget(self.installed_indicator)

        self.install_push_button = QPushButton("Instalar", self.settings_item)
        self.install_push_button.setObjectName("InstallButton")
        self.install_push_button.setVisible(False)  # Initially hidden
        self.settings_item.action_layout.addWidget(self.install_push_button)

    def set_installed(self, installed: bool):
        self.checking_indicator.setVisible(False)
        if installed:
            self.installed_indicator.setVisible(True)
            self.install_push_button.setVisible(False)
        else:
            self.installed_indicator.setVisible(False)
            self.install_push_button.setVisible(True)

    def set_path(self, path: str):
        if not hasattr(self, "horizontal_widget"):
            self.horizontal_widget = QWidget(self.settings_item)
            self.horizontal_widget.setObjectName("HorizontalWidget")
            self.main_layout.addWidget(self.horizontal_widget)

        if not hasattr(self, "horizontal_layout"):
            self.horizontal_layout = QHBoxLayout(self.horizontal_widget)
            self.horizontal_layout.setContentsMargins(20, 10, 20, 10)
            self.horizontal_layout.setSpacing(10)
            self.horizontal_widget.setLayout(self.horizontal_layout)

        if not hasattr(self, "path_label"):
            self.path_label = QLabel(self.settings_item)
            self.path_label.setObjectName("PathLabel")
            self.horizontal_layout.addWidget(self.path_label)

        self.path_label.setText(path)

    def clear_path(self):
        if hasattr(self, "path_label"):
            self.path_label.deleteLater()

        if hasattr(self, "horizontal_layout"):
            self.horizontal_layout.deleteLater()

        if hasattr(self, "horizontal_widget"):
            self.horizontal_widget.deleteLater()

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
