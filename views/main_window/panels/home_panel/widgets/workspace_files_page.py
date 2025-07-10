from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QStyle,
    QStyleOption,
    QLabel,
    QPushButton,
    QButtonGroup,
)
from PySide6.QtGui import QPainter, QIcon
from PySide6.QtCore import Qt, QFile, QTextStream
from views.widgets import ListWidget


class WorkspaceFilesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("FileListWidget")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)
        self.setLayout(self.main_layout)

        # header

        self.header_widget = QWidget(self)
        self.header_widget.setObjectName("FileListWidgetHeader")
        self.main_layout.addWidget(self.header_widget)

        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.header_widget.setLayout(header_layout)

        self.label = QLabel("Archivos", self.header_widget)
        self.label.setObjectName("HeaderLabel")
        header_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.upload_button = QPushButton(self.header_widget)
        self.upload_button.setObjectName("UploadButton")
        self.upload_button.setIcon(QIcon(":/assets/add_file_filled.svg"))
        header_layout.addWidget(
            self.upload_button, alignment=Qt.AlignmentFlag.AlignRight
        )

        # filters

        self.filter_widget = QWidget(self.header_widget)
        self.filter_widget.setObjectName("FilterWidget")
        self.main_layout.addWidget(self.filter_widget)

        filter_layout = QHBoxLayout(self.filter_widget)
        filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_layout.setSpacing(10)
        self.filter_widget.setLayout(filter_layout)

        self.filter_button_group = QButtonGroup(self.filter_widget)
        self.filter_button_group.setObjectName("FilterButtonGroup")
        self.filter_button_group.setExclusive(True)

        self.all_button = QPushButton("Todos", self.filter_widget)
        self.all_button.setObjectName("FilterButton")
        self.all_button.setCheckable(True)
        self.all_button.setChecked(True)
        self.filter_button_group.addButton(self.all_button)
        filter_layout.addWidget(self.all_button)

        self.trimmed_button = QPushButton("Recortados", self.filter_widget)
        self.trimmed_button.setObjectName("FilterButton")
        self.trimmed_button.setCheckable(True)
        self.filter_button_group.addButton(self.trimmed_button)
        filter_layout.addWidget(self.trimmed_button)

        self.krakened_button = QPushButton("Taxonomizado", self.filter_widget)
        self.krakened_button.setObjectName("FilterButton")
        self.krakened_button.setCheckable(True)
        self.filter_button_group.addButton(self.krakened_button)
        filter_layout.addWidget(self.krakened_button)

        """ self.sorted_button = QPushButton("Ordenados", self.filter_widget)
        self.sorted_button.setObjectName("FilterButton")
        self.sorted_button.setCheckable(True)
        self.filter_button_group.addButton(self.sorted_button)
        filter_layout.addWidget(self.sorted_button)

        self.analyzed_button = QPushButton("Analizados", self.filter_widget)
        self.analyzed_button.setObjectName("FilterButton")
        self.analyzed_button.setCheckable(True)
        self.filter_button_group.addButton(self.analyzed_button)
        filter_layout.addWidget(self.analyzed_button) """

        # scroll area

        self.list_widget = ListWidget(self)
        self.main_layout.addWidget(self.list_widget)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
        super().paintEvent(event)
