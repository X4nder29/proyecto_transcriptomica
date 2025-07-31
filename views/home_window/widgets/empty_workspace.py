from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, QFile, QTextStream


class EmptyWorkspace(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName("EmptyWorkspace")

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("Welcome to TranscriptoHub")
        title_label.setObjectName("TitleLabel")
        main_layout.addWidget(title_label, alignment=Qt.AlignHCenter)

        indication_label = QLabel("Open existing workspace from disk")
        indication_label.setObjectName("IndicationLabel")
        main_layout.addWidget(indication_label, alignment=Qt.AlignHCenter)

        main_layout.addSpacing(25)

        # Buttons area

        buttons_area = QWidget()
        buttons_area.setObjectName("ButtonArea")
        main_layout.addWidget(buttons_area)

        button_area_layout = QHBoxLayout(buttons_area)
        button_area_layout.setContentsMargins(0, 0, 0, 0)
        button_area_layout.setSpacing(20)

        # Create Button

        create_button_area = QWidget(buttons_area)
        create_button_area.setObjectName("CreateButtonArea")
        button_area_layout.addWidget(create_button_area, alignment=Qt.AlignHCenter)

        create_button_area_layout = QVBoxLayout(create_button_area)
        create_button_area_layout.setContentsMargins(0, 0, 0, 0)
        create_button_area_layout.setSpacing(0)

        self.create_button = QPushButton(create_button_area)
        self.create_button.setObjectName("CreateWorkspaceButton")
        self.create_button.setIcon(QIcon(":/assets/add.svg"))
        self.create_button.setIconSize(QSize(24, 24))
        self.create_button.setFixedSize(64, 64)
        create_button_area_layout.addWidget(self.create_button, alignment=Qt.AlignHCenter)

        create_label = QLabel("Create new workspace", create_button_area)
        create_label.setObjectName("ButtonName")
        create_button_area_layout.addWidget(create_label, alignment=Qt.AlignHCenter)

        # Open Button

        open_button_area = QWidget(buttons_area)
        open_button_area.setObjectName("OpenButtonArea")
        button_area_layout.addWidget(open_button_area, alignment=Qt.AlignHCenter)

        open_button_area_layout = QVBoxLayout(open_button_area)
        open_button_area_layout.setContentsMargins(0, 0, 0, 0)
        open_button_area_layout.setSpacing(0)

        self.open_button = QPushButton(open_button_area)
        self.open_button.setObjectName("OpenWorkspaceButton")
        self.open_button.setIcon(QIcon(":/assets/folder.svg"))
        self.open_button.setIconSize(QSize(24, 24))
        self.open_button.setFixedSize(64, 64)
        open_button_area_layout.addWidget(self.open_button, alignment=Qt.AlignHCenter)

        open_label = QLabel("Open existing workspace")
        open_label.setObjectName("ButtonName")
        open_button_area_layout.addWidget(open_label, alignment=Qt.AlignHCenter)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
