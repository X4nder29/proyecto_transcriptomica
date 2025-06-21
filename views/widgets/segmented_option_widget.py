from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QButtonGroup,
)
from PySide6.QtCore import QFile, QTextStream
from .option_widget import OptionWidget


class SegmentedOptionWidget(OptionWidget):
    def __init__(self, title: str, options: list[str], parent: QWidget = None):
        self.options = options
        super().__init__(parent=parent, title=title, checkable=False)

    def setup_ui(self):
        super().setup_ui()
        self.body = QWidget(self)
        self.body.setObjectName("Body")
        self.main_layout.addWidget(self.body)

        self.body_layout = QHBoxLayout(self.body)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(10)
        self.body.setLayout(self.body_layout)

        self.button_group = QButtonGroup(self.body)
        self.button_group.setObjectName("SegmentedOptionButtonGroup")
        self.button_group.setExclusive(True)
        self.button_group.setId(self.help_button, 0)

        for index, option in enumerate(self.options):
            button = QPushButton(option, self.body)
            button.setObjectName("SegmentedButton")
            button.setCheckable(True)
            button.setChecked(index == 0)  # Check the first button by default
            button.setToolTip(f"{option} Option")
            self.button_group.addButton(button, id=index + 1)
            self.body_layout.addWidget(button)

    def load_stylesheet(self):
        super().load_stylesheet()
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(self.styleSheet() + "\n" + stylesheet)
            qss_file.close()
