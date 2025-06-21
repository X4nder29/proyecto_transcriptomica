from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QSpacerItem,
    QFrame,
    QStyleOption,
    QStyle,
    QScrollArea,
    QSizePolicy,
)
from PySide6.QtGui import QIcon, QPainter
from PySide6.QtCore import Qt, QFile, QTextStream


class Workspaces(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("Workspaces")

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setStretch(2, 1)

        # header area

        self.header_area = QWidget(self)
        self.header_area.setObjectName("HeaderArea")
        self.main_layout.addWidget(
            self.header_area, alignment=Qt.AlignmentFlag.AlignTop
        )

        self.header_area_layout = QHBoxLayout(self.header_area)
        self.header_area_layout.setContentsMargins(20, 0, 20, 0)
        self.header_area_layout.setSpacing(0)

        self.search_icon_label = QLabel(self.header_area)
        self.search_icon_label.setObjectName("SearchIconLabel")
        self.search_icon_label.setPixmap(QIcon(":/assets/search.svg").pixmap(20, 20))
        self.header_area_layout.addWidget(self.search_icon_label)

        self.header_area_layout.addItem(QSpacerItem(5, 0))

        self.search_line_edit = QLineEdit(self.header_area)
        self.search_line_edit.setObjectName("SearchLineEdit")
        self.search_line_edit.setPlaceholderText("Search workspaces...")
        self.search_line_edit.setMinimumHeight(30)
        self.header_area_layout.addWidget(self.search_line_edit)

        self.header_area_layout.addItem(QSpacerItem(5, 0))

        self.create_new_workspace_button = QPushButton(self.header_area)
        self.create_new_workspace_button.setObjectName("CreateNewWorkspaceButton")
        self.create_new_workspace_button.setText("New Workspace")
        self.create_new_workspace_button.setFixedHeight(self.search_line_edit.height())
        self.header_area_layout.addWidget(self.create_new_workspace_button)

        self.header_area_layout.addItem(QSpacerItem(5, 0))

        self.open_existing_workspace_button = QPushButton(self.header_area)
        self.open_existing_workspace_button.setObjectName("OpenExistingWorkspaceButton")
        self.open_existing_workspace_button.setText("Open")
        self.open_existing_workspace_button.setFixedHeight(
            self.search_line_edit.height()
        )
        self.header_area_layout.addWidget(self.open_existing_workspace_button)

        # spacer

        horizontal_spacer = QFrame(self)
        horizontal_spacer.setFrameShape(QFrame.HLine)
        horizontal_spacer.setFrameShadow(QFrame.Sunken)
        horizontal_spacer.setObjectName("HorizontalSpacer")

        self.main_layout.addWidget(
            horizontal_spacer, alignment=Qt.AlignmentFlag.AlignTop
        )

        # body area

        self.body_area = QWidget(self)
        self.body_area.setObjectName("BodyArea")
        self.main_layout.addWidget(self.body_area, 1)

        self.body_area_layout = QVBoxLayout(self.body_area)
        self.body_area_layout.setContentsMargins(0, 0, 0, 0)
        self.body_area_layout.setSpacing(0)

        # workspaces list

        self.workspaces_list = QWidget(self.body_area)
        self.workspaces_list.setObjectName("WorkspacesList")
        self.workspaces_list.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.workspaces_list_layout = QVBoxLayout(self.workspaces_list)
        self.workspaces_list_layout.setContentsMargins(0, 0, 0, 0)
        self.workspaces_list_layout.setSpacing(0)
        self.workspaces_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.workspaces_scroll_area = QScrollArea(self.body_area)
        self.workspaces_scroll_area.setObjectName("WorkspacesScrollArea")
        self.workspaces_scroll_area.setWidgetResizable(True)
        self.workspaces_scroll_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.workspaces_scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.workspaces_scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.workspaces_scroll_area.setWidget(self.workspaces_list)
        self.body_area_layout.addWidget(self.workspaces_scroll_area)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def paintEvent(self, _):
        option = QStyleOption()
        option.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)
