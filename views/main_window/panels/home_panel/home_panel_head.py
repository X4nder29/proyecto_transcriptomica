from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from views.widgets import PanelHeadBase, ActionButtonWidget


class HomePanelHead(PanelHeadBase):

    def __init__(self, parent: QWidget = None):
        super().__init__("TranscriptoHub", parent)

    def setup_ui(self):
        super().setup_ui()

        # user manual button

        self.user_manual_button = ActionButtonWidget(
            icon_path=":/assets/user_manual.svg",
            tooltip="Abrir manual de usuario",
            parent=self,
        )
        self.user_manual_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.main_layout.addWidget(self.user_manual_button)
