from pathlib import Path
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, QFile, QTextStream
from .settings_item import SettingsItem


class InstalledDependencyItem(SettingsItem):
    def __init__(self, icon, title, subtitle, parent=None):
        super().__init__(icon, title, subtitle, parent)

    def setup_ui(self):
        super().setup_ui()

        self.checking_indicator = QLabel("Comprobando...")
        self.checking_indicator.setObjectName("CheckingIndicator")
        self.action_layout.addWidget(self.checking_indicator)

        self.installed_indicator = QLabel("Instalado")
        self.installed_indicator.setObjectName("InstalledIndicator")
        self.installed_indicator.setVisible(False)
        self.action_layout.addWidget(self.installed_indicator)

        self.install_push_button = QPushButton("Instalar")
        self.install_push_button.setObjectName("InstallButton")
        self.install_push_button.setVisible(False)  # Initially hidden
        self.action_layout.addWidget(self.install_push_button)

    def set_installed(self, installed: bool):
        self.checking_indicator.setVisible(False)

        if installed:
            self.installed_indicator.setVisible(True)
            self.install_push_button.setVisible(False)
        else:
            self.installed_indicator.setVisible(False)
            self.install_push_button.setVisible(True)

    def load_stylesheet(self, scheme: Qt.ColorScheme):
        super().load_stylesheet(QGuiApplication.styleHints().colorScheme())
        qss_file = QFile(
            f":/styles/{Path(__file__).stem}_{"dark" if scheme == Qt.ColorScheme.Dark else "light"}.qss"
        )
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(self.styleSheet() + stylesheet)
            style = self.style()
            style.unpolish(self)
            style.polish(self)
            self.update()
            qss_file.close()
