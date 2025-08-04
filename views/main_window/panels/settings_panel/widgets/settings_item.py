from pathlib import Path
from typing import Optional
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStyleOption,
    QStyle,
    QLabel,
)
from PySide6.QtGui import QGuiApplication, QPainter, QIcon
from PySide6.QtCore import Qt, QFile, QTextStream


class SettingsItem(QWidget):
    def __init__(
        self, icon: QIcon, title: str, subtitle: Optional[str] = None, parent: QWidget = None
    ):
        super().__init__(parent)
        self.icon = icon
        self.title = title
        self.subtitle = subtitle
        self.load_stylesheet(QGuiApplication.styleHints().colorScheme())
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)

    def setup_ui(self):
        self.setObjectName("SettingsItem")
        self.setMaximumWidth(1000)

        # Layout horizontal principal
        horizontal_layout = QHBoxLayout(self)
        horizontal_layout.setContentsMargins(20, 10, 20, 10)
        horizontal_layout.setSpacing(20)

        # Icono
        lbl_icon = QLabel()
        lbl_icon.setPixmap(self.icon.pixmap(18, 18))
        horizontal_layout.addWidget(lbl_icon)

        # Textos (título + subtítulo)
        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(2)
        horizontal_layout.addLayout(vertical_layout)

        lbl_title = QLabel(self.title)
        lbl_title.setObjectName("SettingsItemTitle")
        vertical_layout.addWidget(lbl_title)

        if self.subtitle:
            lbl_sub = QLabel(self.subtitle)
            lbl_sub.setObjectName("SettingsItemSubtitle")
            vertical_layout.addWidget(lbl_sub)

        horizontal_layout.addStretch()

        self.action_layout = QHBoxLayout()
        self.action_layout.setContentsMargins(0, 0, 0, 0)
        self.action_layout.setSpacing(10)
        horizontal_layout.addLayout(self.action_layout)

    def load_stylesheet(self, scheme: Qt.ColorScheme):
        qss_file = QFile(
            f":/styles/{Path(__file__).stem}_{"dark" if scheme == Qt.ColorScheme.Dark else "light"}.qss"
        )
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            style = self.style()
            style.unpolish(self)
            style.polish(self)
            self.update()
            qss_file.close()

    def paintEvent(self, _):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
