from PySide6.QtWidgets import (
    QWidget,
    QAbstractButton,
    QSizePolicy,
    QVBoxLayout,
    QHBoxLayout,
    QStyle,
    QStyleOption,
    QLabel,
)
from PySide6.QtGui import QPainter, QIcon
from PySide6.QtCore import Qt, Property, QTimer


class ItemAbstractButton(QAbstractButton):

    checked = Property(bool, QAbstractButton.isChecked, QAbstractButton.setChecked)

    def __init__(self, icon: str, parent=None):
        super().__init__(parent)
        self.icon = icon
        self.setup_ui()
        self.setProperty("checked", False)
        self.toggled.connect(self._update_style)
        self._resize_timer = QTimer()
        self._resize_timer.setSingleShot(True)

    def setup_ui(self):
        self.setObjectName("ItemAbstractButton")
        self.setMinimumWidth(300)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCheckable(True)
        self.setChecked(False)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(20, 10, 10, 10)
        self.main_layout.setSpacing(20)
        self.setLayout(self.main_layout)

        self.icon_label = QLabel(self)
        self.icon_label.setObjectName("IconLabel")
        self.icon_label.setPixmap(QIcon(self.icon).pixmap(18, 18))
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(
            self.icon_label, alignment=Qt.AlignmentFlag.AlignLeft
        )

        # Content area

        self.content_area = QWidget(self)
        self.content_area.setObjectName("ContentWidget")
        self.content_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.main_layout.addWidget(self.content_area)

        self.content_area_layout = QVBoxLayout(self.content_area)
        self.content_area_layout.setContentsMargins(0, 0, 0, 0)
        self.content_area_layout.setSpacing(5)
        self.content_area.setLayout(self.content_area_layout)

        # Space

        self.main_layout.addStretch()

        # Action area

        self.action_area = QWidget(self)
        self.action_area.setObjectName("ActionAreaWidget")
        self.main_layout.addWidget(self.action_area)

        self.action_area_layout = QHBoxLayout(self.action_area)
        self.action_area_layout.setContentsMargins(0, 0, 0, 0)
        self.action_area_layout.setSpacing(5)
        self.action_area.setLayout(self.action_area_layout)

    def _update_style(self, checked: bool):
        self.setProperty("checked", checked)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._resize_timer.start(50)

    def paintEvent(self, _):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
