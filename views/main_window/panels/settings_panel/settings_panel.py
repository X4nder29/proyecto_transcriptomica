from PySide6.QtWidgets import QWidget, QSizePolicy, QVBoxLayout
from PySide6.QtCore import Qt
from .settings_panel_head import SettingsPanelHead
from .settings_panel_body import SettingsPanelBody


class SettingsPanel(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("SettingsPanel")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.main_layout)

        self.header = SettingsPanelHead(self)
        self.main_layout.addWidget(self.header)

        self.content = SettingsPanelBody(self)
        self.main_layout.addWidget(self.content)
