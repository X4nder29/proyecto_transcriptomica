from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QLabel,
    QStyleOption,
    QStyle,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from .number_selector import NumberSelector


class SlidingWindowOption(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("SlidingWindowOption")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setupUi()

    def setupUi(self):

        self.setMinimumWidth(350)
        self.setMinimumHeight(150)
        self.setStyleSheet(
            """
            QWidget#SlidingWindowOption {
                background-color: #404040;
                border-radius: 10px;
            }
            """
        )

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # head

        self.title = QLabel("SlidingWindow", self)
        self.title.setObjectName("title")
        self.title.setStyleSheet(
            """
            QLabel#title {
                font-size: 14px;
                font-weight: bold;
                color: white;
            }
            """
        )

        # body

        self.body = QWidget(self)
        self.body.setObjectName("body")

        self.body_layout = QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(10)

        # bases window size area

        self.bases_window_size_area = QWidget(self.body)
        self.bases_window_size_area.setObjectName("bases_window_size_area")

        self.value_area_layout = QHBoxLayout(self.bases_window_size_area)
        self.value_area_layout.setContentsMargins(0, 0, 0, 0)
        self.value_area_layout.setSpacing(20)

        self.bases_window_size_label = QLabel("Bases Window Size", self.bases_window_size_area)
        self.bases_window_size_label.setObjectName("bases_window_size_label")
        self.bases_window_size_label.setStyleSheet(
            """
            QLabel#bases_window_size_label {
                font-size: 12px;
                color: white;
            }
            """
        )

        self.value_area_layout.addWidget(self.bases_window_size_label)

        self.value_number_selector = NumberSelector(self.bases_window_size_area)

        self.value_area_layout.addWidget(self.value_number_selector)

        self.body_layout.addWidget(self.bases_window_size_area)

        # average quality area

        self.average_quality_area = QWidget(self.body)
        self.average_quality_area.setObjectName("average_quality_area")

        self.average_quality_area_layout = QHBoxLayout(self.average_quality_area)
        self.average_quality_area_layout.setContentsMargins(0, 0, 0, 0)
        self.average_quality_area_layout.setSpacing(20)

        self.average_quality_label = QLabel("Average Quality", self.average_quality_area)
        self.average_quality_label.setObjectName("average_quality_label")
        self.average_quality_label.setStyleSheet(
            """
            QLabel#average_quality_label {
                font-size: 12px;
                color: white;
            }
            """
        )

        self.average_quality_area_layout.addWidget(self.average_quality_label)

        self.average_quality_number_selector = NumberSelector(self.average_quality_area)

        self.average_quality_area_layout.addWidget(self.average_quality_number_selector)

        self.body_layout.addWidget(self.average_quality_area)

        #

        self.main_layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignTop)

        self.main_layout.addWidget(self.body)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
