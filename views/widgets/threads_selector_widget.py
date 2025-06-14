import os
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStyleOption,
    QStyle,
    QSlider,
    QLabel,
    QPushButton,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QFile, QTextStream


class ThreadsSelectorWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("ThreadsSelectorWidget")
        self.setMinimumWidth(300)

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        ## header

        self.header = QWidget(self)
        self.header.setObjectName("Header")
        self.main_layout.addWidget(self.header)

        self.header_layout = QHBoxLayout(self.header)
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setSpacing(0)

        # title

        self.title = QLabel("Threads", self.header)
        self.title.setObjectName("OptionTitle")
        self.header_layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignLeft)

        # space

        self.header_layout.addStretch()

        # help

        self.help = QPushButton("?", self.header)
        self.help.setObjectName("HelpButton")
        self.help.setToolTip("Select the number of threads to use for processing.")
        self.header_layout.addWidget(self.help, alignment=Qt.AlignmentFlag.AlignRight)

        ## body

        self.slider = QSlider(Qt.Horizontal, self)
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
