from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
)
from PySide6.QtCore import Qt, QFile, QTextStream
from views.widgets import ItemWidget, ItemActionWidget


class DatabaseItemWidget(ItemWidget):
    def __init__(
        self, name: str, link: str, parent: QWidget = None, installed: bool = False
    ):
        self.name = name
        self.link = link
        self.installed = installed
        super().__init__(":/assets/database.svg", parent=parent)
        self.load_stylesheet()

    def setup_ui(self):
        super().setup_ui()
        self.setObjectName("DatabaseItemWidget")

        self.name_label = QLabel(self.name, self.content_area)
        self.name_label.setObjectName("NameLabel")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.content_area_layout.addWidget(self.name_label)

        self.link_label = QLabel(self.link, self.content_area)
        self.link_label.setObjectName("LinkLabel")
        self.link_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.content_area_layout.addWidget(self.link_label)

        if not self.installed:
            self.install_action = ItemActionWidget(
                ":/assets/download.svg", self.action_area
            )
            self.install_action.setToolTip("Install Database")
            self.action_area_layout.addWidget(self.install_action)
        else:
            self.open_action = ItemActionWidget(":/assets/folder.svg", self.action_area)
            self.open_action.setToolTip("Open Database Folder")
            self.action_area_layout.addWidget(self.open_action)

        self.delete_action = ItemActionWidget(":/assets/trash.svg", self.action_area)
        self.delete_action.setToolTip("Delete Database")
        self.action_area_layout.addWidget(self.delete_action)

    def set_name(self, name: str):
        self.name = name
        self.name_label.setText(name)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
