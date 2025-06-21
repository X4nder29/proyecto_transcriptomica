from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStyleOption,
    QStyle,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QFile, QTextStream
from views.widgets import SelectFilePushButton


class PairedInputFileWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("PairedInputFileWidget")

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        self.setLayout(self.main_layout)

        self.head_widget = QWidget(self)
        self.head_widget.setObjectName("HeadWidget")
        self.main_layout.addWidget(
            self.head_widget, alignment=Qt.AlignmentFlag.AlignTop
        )

        self.head_widget_layout = QHBoxLayout(self.head_widget)
        self.head_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.head_widget_layout.setSpacing(0)
        self.head_widget.setLayout(self.head_widget_layout)

        self.input_file_title_label_1 = QLabel(self.head_widget)
        self.input_file_title_label_1.setObjectName("TitleLabel")
        self.input_file_title_label_1.setText("Archivo de entrada 1")
        self.head_widget_layout.addWidget(
            self.input_file_title_label_1, alignment=Qt.AlignmentFlag.AlignLeft
        )

        self.head_widget_layout.addStretch()

        self.help_push_button = QPushButton(self.head_widget)
        self.help_push_button.setObjectName("HelpButton")
        self.help_push_button.setText("?")
        self.head_widget_layout.addWidget(
            self.help_push_button, alignment=Qt.AlignmentFlag.AlignRight
        )

        self.select_file_push_button_1 = SelectFilePushButton(self)
        self.main_layout.addWidget(self.select_file_push_button_1)

        self.input_file_title_label_2 = QLabel(self.head_widget)
        self.input_file_title_label_2.setObjectName("TitleLabel")
        self.input_file_title_label_2.setText("Archivo de entrada 2")
        self.main_layout.addWidget(
            self.input_file_title_label_2, alignment=Qt.AlignmentFlag.AlignLeft
        )

        self.select_file_push_button_2 = SelectFilePushButton(self)
        self.main_layout.addWidget(self.select_file_push_button_2)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def paintEvent(self, _):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
        super().paintEvent(_)
