from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from views.widgets import PanelHeadBase, ActionButtonWidget


class TrimmomaticPanelHead(PanelHeadBase):

    def __init__(self, parent: QWidget = None):
        super().__init__("Trimmomatic", parent=parent)

    def setup_ui(self):
        super().setup_ui()
        self.setObjectName("TrimmomaticPanelHead")

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
        self.cli_push_button.setVisible(False) # Initially hidden
        self.main_layout.addWidget(self.cli_push_button)

        # star button
        self.star_button = ActionButtonWidget(
            icon_path=":/assets/filled_star.svg",
            tooltip="Marcar como favorito",
            parent=self,
        )
        self.star_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.star_button.setVisible(False) # Initially hidden
        self.main_layout.addWidget(self.star_button)
