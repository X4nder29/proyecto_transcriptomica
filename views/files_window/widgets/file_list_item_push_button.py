from pathlib import Path
from textwrap import shorten
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStyleOption,
    QStyle,
    QSizePolicy,
    QLabel,
    QPushButton,
)
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import Qt, QFile, QTextStream


class FileListItemPushButton(QPushButton):
    def __init__(self, file_name: str, file_path: str, parent=None):
        super().__init__(parent)

        self.file_name = file_name
        self.file_path = file_path
        self.setObjectName("FileListItemPushButton")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setToolTip(self.file_path)

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        self.setLayout(self.main_layout)

        self.trailing_icon = QLabel(self)
        self.trailing_icon.setObjectName("TrailingIcon")
        self.trailing_icon.setPixmap(
            QPixmap(":/assets/file.svg").scaled(
                22,
                22,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.main_layout.addWidget(
            self.trailing_icon, alignment=Qt.AlignmentFlag.AlignLeft
        )

        self.content_widget = QWidget(self)
        self.content_widget.setObjectName("ContentWidget")
        self.main_layout.addWidget(
            self.content_widget, alignment=Qt.AlignmentFlag.AlignLeft
        )

        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        self.title_label = QLabel(self.file_name, self)
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.content_layout.addWidget(self.title_label)

        self.path_label = QLabel(
            shorten(self.file_path, width=100, placeholder="..."), self
        )
        self.path_label.setObjectName("PathLabel")
        self.path_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.content_layout.addWidget(self.path_label)

        self.main_layout.addStretch()

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def sizeHint(self):
        return self.layout().sizeHint()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
        super().paintEvent(event)
