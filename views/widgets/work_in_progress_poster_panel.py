from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QLabel,
    QStyleOption,
    QStyle,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QIcon
from pathlib import Path


class WorkInProgressPosterPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("WorkInProgressPosterPanel")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_style_sheet()
        self.setup_ui()

    def setup_ui(self):

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        self.text_area = QWidget(self)
        self.text_area.setObjectName("TextArea")
        self.text_area.setFixedWidth(300)

        self.text_area_layout = QVBoxLayout(self.text_area)
        self.text_area_layout.setContentsMargins(20, 20, 20, 20)
        self.text_area_layout.setSpacing(10)
        self.text_area.setLayout(self.text_area_layout)

        self.icon_label = QLabel(self.text_area)
        self.icon_label.setObjectName("Icon")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setPixmap(
            QIcon("assets/work_in_progress.svg").pixmap(32, 32)
        )
        self.text_area_layout.addWidget(
            self.icon_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.text_label = QLabel("Work in progress", self.text_area)
        self.text_label.setObjectName("TextLabel")
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_area_layout.addWidget(
            self.text_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.main_layout.addWidget(
            self.text_area, alignment=Qt.AlignmentFlag.AlignCenter
        )

    def load_style_sheet(self):
        styles_path = Path(__file__).parent / "work_in_progress_poster_panel.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
