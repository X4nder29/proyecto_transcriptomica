from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSlider,
    QLabel,
    QStyleOption,
    QStyle,
)
from PySide6.QtCore import Qt, QFile, QTextStream
from PySide6.QtGui import QPainter
from pathlib import Path
import os


class ThreadsOption(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("ThreadsOption")

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.title = QLabel("Threads", self)
        self.title.setObjectName("OptionTitle")
        self.main_layout.addWidget(self.title)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(1 if os.cpu_count() is None else os.cpu_count())
        self.slider.setValue(1)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(1)
        self.main_layout.addWidget(self.slider)

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
