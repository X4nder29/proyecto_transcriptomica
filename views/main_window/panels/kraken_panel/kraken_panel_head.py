from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from views.widgets import PanelHeadBase, ActionButtonWidget


class KrakenPanelHead(PanelHeadBase):
    """
    KrakenPanelHead is a QWidget that represents the header of the Kraken panel in the main window.
    It is used to display the title and other header-related functionalities.
    """

    def __init__(self, parent: QWidget = None):
        super().__init__("Kraken", parent=parent)

    def setup_ui(self):
        super().setup_ui()
        self.setObjectName("KrakenPanelHead")

        # cli push button

        self.cli_push_button = ActionButtonWidget(
            icon_path=":/assets/cli_filled.svg",
            tooltip="Visualizar comando a ejecutar",
            parent=self,
        )
        self.cli_push_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.cli_push_button.setVisible(False)  # Initially hidden
        self.main_layout.addWidget(self.cli_push_button)

        # star button

        self.star_button = ActionButtonWidget(
            icon_path=":/assets/filled_star.svg",
            tooltip="Marcar como favorito",
            parent=self,
        )
        self.star_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.star_button.setVisible(False)  # Initially hidden
        self.main_layout.addWidget(self.star_button)

        # database button

        self.database_download_manager_button = ActionButtonWidget(
            icon_path=":/assets/database.svg",
            tooltip="Abrir gestor de bases de datos",
            parent=self,
        )
        self.database_download_manager_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.main_layout.addWidget(self.database_download_manager_button)
