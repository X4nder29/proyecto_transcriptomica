from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QLabel,
    QScrollArea,
from PySide6.QtCore import Qt, QFile, QTextStream
from pathlib import Path
from .file_list_item import FileListItem


class FileList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("FileList")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        self.title = QLabel("Files", self)
        self.title.setObjectName("FileListTitle")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.title)

        self.file_list_widget = QWidget(self)
        self.file_list_layout = QVBoxLayout(self.file_list_widget)
        self.file_list_layout.setContentsMargins(0, 0, 0, 0)
        self.file_list_layout.setSpacing(0)

        self.file_list_area = QScrollArea(self)
        self.file_list_area.setObjectName("FileListScrollArea")
        self.file_list_area.setWidgetResizable(True)
        self.file_list_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.file_list_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.file_list_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.file_list_area.setWidget(self.file_list_widget)
        self.main_layout.addWidget(self.file_list_area)

        for i in range(15):
            file_item = FileListItem(f"File {i + 1}", f"/path/to/file_{i + 1}.txt", self.file_list_area)
    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
