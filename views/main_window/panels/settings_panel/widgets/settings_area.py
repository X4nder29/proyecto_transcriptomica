from typing import Optional
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QStyleOption,
    QStyle,
    QLabel,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import QFile, QTextStream
from .settings_item import SettingsItem


class SettingsArea(QWidget):
    def __init__(self, parent: QWidget = None, title: Optional[str] = None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
        self.load_stylesheet()

    def setup_ui(self):
        self.setObjectName("SettingsArea")
        self.setMaximumWidth(1000)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        self.setLayout(main_layout)

        if self.title is not None:
            label = QLabel(self.title)
            label.setObjectName("SettingsAreaTitle")
            main_layout.addWidget(label)

        items_list = QWidget(self)
        main_layout.addWidget(items_list)

        items_layout = QVBoxLayout(items_list)
        items_layout.setContentsMargins(0, 0, 0, 0)
        items_layout.setSpacing(5)

    def add_item(self, item_widget: SettingsItem):
        self.layout().addWidget(item_widget)
        item_widget.setParent(self)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def paintEvent(self, _):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
