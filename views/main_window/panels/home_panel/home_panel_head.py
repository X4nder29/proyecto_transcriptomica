from PySide6.QtWidgets import QWidget
from views.widgets import PanelHeadBase


class HomePanelHead(PanelHeadBase):

    def __init__(self, parent: QWidget = None):
        super().__init__("TranscriptoHub", parent)
