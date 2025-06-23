from pathlib import Path
from PySide6.QtWidgets import (
    QVBoxLayout,
    QStyleOption,
    QStyle,
    QSizePolicy,
    QPushButton,
    QLabel,
)
from PySide6.QtGui import QPainter, QDragEnterEvent, QDropEvent, QPixmap
from PySide6.QtCore import Qt, Signal, QFile, QTextStream


class UploadFilesPushButton(QPushButton):
    dropped = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("UploadFilesPushButton")
        self.setAcceptDrops(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(self.main_layout)

        self.upload_icon_pixmap = QPixmap(":/assets/upload_file.svg")

        self.upload_icon_label = QLabel(self)
        self.upload_icon_label.setObjectName("UploadIcon")
        self.upload_icon_label.setPixmap(self.upload_icon_pixmap)
        self.main_layout.addWidget(self.upload_icon_label, alignment=Qt.AlignCenter)

        self.main_label = QLabel(self)
        self.main_label.setObjectName("MainLabel")
        self.main_label.setText("Drag and drop files here or click to upload")
        self.main_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.main_label, alignment=Qt.AlignCenter)

        self.secondary_label = QLabel(self)
        self.secondary_label.setObjectName("SecondaryLabel")
        self.secondary_label.setText("or choose a files")
        self.secondary_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.secondary_label, alignment=Qt.AlignCenter)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        md = event.mimeData()
        if md.hasText():
            self.dropped.emit(md.text())
            event.acceptProposedAction()
        else:
            event.ignore()

    def sizeHint(self):
        return self.layout().sizeHint()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
        super().paintEvent(event)
