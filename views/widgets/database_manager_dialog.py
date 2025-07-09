from pathlib import Path
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStyle,
    QStyleOption,
    QLabel,
    QPushButton,
    QLineEdit,
    QScrollArea,
    QSizePolicy,
)
from PySide6.QtGui import QPainter, QIcon
from PySide6.QtCore import Qt, QFile, QTextStream


class DatabaseManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_stylesheet()

    def setup_ui(self):
        self.setObjectName("DatabaseManagerDialog")
        self.setWindowTitle("Database Download Manager")
        self.setWindowIcon(QIcon(":/assets/database.svg"))
        self.setMinimumWidth(500)
        self.setWindowModality(Qt.WindowModality.WindowModal)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.main_layout)

        # header

        self.header_widget = QWidget(self)
        self.header_widget.setObjectName("HeaderWidget")
        self.main_layout.addWidget(self.header_widget)

        self.header_layout = QHBoxLayout(self.header_widget)
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setSpacing(10)
        self.header_widget.setLayout(self.header_layout)

        self.link_line_edit = QLineEdit(self.header_widget)
        self.link_line_edit.setObjectName("LinkLineEdit")
        self.link_line_edit.setPlaceholderText("Enter database link")
        self.link_line_edit.setClearButtonEnabled(True)
        self.header_layout.addWidget(self.link_line_edit)

        self.add_button = QPushButton(self.header_widget)
        self.add_button.setObjectName("AddButton")
        self.add_button.setToolTip("Add database link")
        self.add_button.setIcon(QIcon(":/assets/add.svg"))
        self.header_layout.addWidget(self.add_button)

        # installed

        self.installed_label = QLabel("Installed", self)
        self.installed_label.setObjectName("InstalledLabel")
        self.installed_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.installed_label)

        self.installed_scroll_area = QScrollArea(self)
        self.installed_scroll_area.setObjectName("InstalledScrollArea")
        self.installed_scroll_area.setWidgetResizable(True)
        self.installed_scroll_area.setMinimumWidth(350)
        self.installed_scroll_area.setMaximumHeight(200)
        self.installed_scroll_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.installed_scroll_area.setVisible(False)
        self.main_layout.addWidget(self.installed_scroll_area)

        self.installed_widget = QWidget(self.installed_scroll_area)
        self.installed_widget.setObjectName("installedWidget")

        self.installed_scroll_area.setWidget(self.installed_widget)

        self.installed_layout = QVBoxLayout(self.installed_widget)
        self.installed_layout.setContentsMargins(0, 0, 10, 0)
        self.installed_layout.setSpacing(10)
        self.installed_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.installed_widget.setLayout(self.installed_layout)

        # uninstalled

        self.uninstalled_label = QLabel("Uninstalled", self)
        self.uninstalled_label.setObjectName("UninstalledLabel")
        self.uninstalled_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(
            self.uninstalled_label, alignment=Qt.AlignmentFlag.AlignTop
        )

        self.uninstalled_scroll_area = QScrollArea(self)
        self.uninstalled_scroll_area.setObjectName("UninstalledScrollArea")
        self.uninstalled_scroll_area.setWidgetResizable(True)
        self.uninstalled_scroll_area.setMinimumWidth(350)
        self.uninstalled_scroll_area.setMaximumHeight(200)
        self.uninstalled_scroll_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.uninstalled_scroll_area.setVisible(False)
        self.main_layout.addWidget(
            self.uninstalled_scroll_area, 1, alignment=Qt.AlignmentFlag.AlignTop
        )

        self.uninstalled_widget = QWidget(self.uninstalled_scroll_area)
        self.uninstalled_widget.setObjectName("uninstalledWidget")
        self.uninstalled_scroll_area.setWidget(self.uninstalled_widget)

        self.uninstalled_layout = QVBoxLayout(self.uninstalled_widget)
        self.uninstalled_layout.setContentsMargins(0, 0, 10, 0)
        self.uninstalled_layout.setSpacing(10)
        self.uninstalled_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.uninstalled_widget.setLayout(self.uninstalled_layout)

        # add stretch
        self.main_layout.addStretch()

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def paintEvent(self, _):
        super().paintEvent(_)
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
