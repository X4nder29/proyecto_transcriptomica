from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QLabel,
    QStyle,
    QStyleOption,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from pathlib import Path


class FileListItem(QWidget):

    def __init__(self, name, path, parent=None):
        super().__init__(parent)

        self.name = name
        self.path = path

        self.setObjectName("FileListItem")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_style_sheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(0)

        # file name
        self.name_label = QLabel(self.name, self)
        self.name_label.setObjectName("FileListItemTitle")
        self.main_layout.addWidget(self.name_label)

        # file path
        self.paht_label = QLabel(self.path, self)
        self.paht_label.setObjectName("FileListItemPath")
        self.main_layout.addWidget(self.paht_label)

        # body widgets setup can be added here

        self.setLayout(self.main_layout)

    def load_style_sheet(self):
        styles_path = Path(__file__).parent / "file_list_item.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
