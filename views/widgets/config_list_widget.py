from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QStyleOption,
    QStyle,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QFile, QTextStream


class ConfigListWidget(QWidget):

    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        self.name = name
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("ConfigListWidget")
        self.setMinimumWidth(300)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.main_layout)

        # Name

        self.name_label = QLabel("Configuraciones Guardadas", self)
        self.name_label.setObjectName("NameLabel")
        self.main_layout.addWidget(self.name_label)

        # List

        self.list_scroll_area = QScrollArea(self)
        self.list_scroll_area.setObjectName("ListScrollArea")
        self.list_scroll_area.setWidgetResizable(True)
        self.list_scroll_area.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.list_scroll_area)

        self.list_widget = QWidget(self.list_scroll_area)
        self.list_widget.setObjectName("ListWidget")
        self.list_scroll_area.setWidget(self.list_widget)

        self.list_layout = QVBoxLayout(self.list_widget)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(10)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.list_widget.setLayout(self.list_layout)

        """ for i in range(5):
            config_item_widget = ConfigItemWidget(f"Configuración {i + 1}", parent=self.list_widget)
            self.list_layout.addWidget(config_item_widget) """

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
