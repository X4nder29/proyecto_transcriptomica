from PySide6.QtWidgets import QWidget
from views.widgets import PanelHeadBase


class SettingsPanelHead(PanelHeadBase):

    def __init__(self, parent: QWidget = None):
        super().__init__("Configuraciones", parent=parent)

    def setup_ui(self):
        super().setup_ui()
        self.setObjectName("SettingsPanelHead")
