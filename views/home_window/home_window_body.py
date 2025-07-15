from PySide6.QtWidgets import QWidget, QStackedLayout
from .widgets import EmptyWorkspace
from .widgets import Workspaces


class HomeWindowBody(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("HomeWindowBody")

        self.main_layout = QStackedLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # empty workspace

        self.empty_workspace = EmptyWorkspace(self)
        self.empty_workspace.setObjectName("EmptyWorkspace")
        self.main_layout.addWidget(self.empty_workspace)

        # workspaces

        self.workspaces = Workspaces(self)
        self.workspaces.setObjectName("Workspaces")
        self.main_layout.addWidget(self.workspaces)
