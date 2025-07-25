from pathlib import Path
from typing import Optional
from PySide6.QtWidgets import (
    QWidget,
    QStyleOption,
    QStyle,
    QPushButton,
)
from PySide6.QtGui import QPainter, QIcon
from PySide6.QtCore import QFile, QTextStream
from .settings_item import SettingsItem


class SimpleActionItem(SettingsItem):
    def __init__(
        self,
        icon: QIcon,
        title: str,
        action: str,
        subtitle: Optional[str] = None,
        parent: Optional[QWidget] = None,
    ):
        self.action = action
        super().__init__(icon, title, subtitle, parent)

    def setup_ui(self):
        super().setup_ui()

        self.open_manual_push_button = QPushButton(self.action)
        self.action_layout.addWidget(self.open_manual_push_button)

    def load_stylesheet(self):
        super().load_stylesheet()
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(self.styleSheet() + f"\n{stylesheet}")
            qss_file.close()

    def paintEvent(self, _):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
