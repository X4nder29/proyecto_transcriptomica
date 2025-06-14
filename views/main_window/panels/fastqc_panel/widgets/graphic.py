import base64
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QStyle,
    QStyleOption,
    QLabel,
)
from PySide6.QtCore import Qt, QFile, QTextStream
from PySide6.QtGui import QPainter, QPixmap
from pathlib import Path


class Graphic(QWidget):

    def __init__(self, title, image, parent=None):
        super().__init__(parent)

        self.title = title
        self.image = image

        self.setObjectName("Graphic")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        # graphic name

        self.title_label = QLabel(self.title, self)
        self.title_label.setObjectName("GraphicTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        # graphic image

        if self.image.startswith("data:image"):

            self.image = self.image.split(",")[1]
            self.image = base64.b64decode(self.image)

            self.image_pixmap = QPixmap()
            self.image_pixmap.loadFromData(self.image)

            self.image_label = QLabel(self)
            self.image_label.setObjectName("GraphicImage")
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.image_label.setPixmap(self.image_pixmap.scaledToWidth(325, Qt.TransformationMode.SmoothTransformation))
            """ self.image_label.setScaledContents(True) """
            self.main_layout.addWidget(self.image_label)

        self.setLayout(self.main_layout)

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
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
