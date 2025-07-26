from PySide6.QtCore import Qt
from views.widgets import PanelHeadBase, ActionButtonWidget


class FastqcPanelHead(PanelHeadBase):

    def __init__(self, parent=None):
        super().__init__("FastQC", parent)

    def setup_ui(self):
        super().setup_ui()

        # user manual button

        self.user_manual_button = ActionButtonWidget(
            icon_path=":/assets/user_manual.svg",
            tooltip="Manual de usuario",
            parent=self,
        )
        self.user_manual_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.main_layout.addWidget(self.user_manual_button)

        # cli push button

        self.cli_push_button = ActionButtonWidget(
            icon_path=":/assets/cli_filled.svg",
            tooltip="Visualizar comando a ejecutar",
            parent=self,
        )
        self.cli_push_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.main_layout.addWidget(self.cli_push_button)
