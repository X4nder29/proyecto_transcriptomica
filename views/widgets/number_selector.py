from pathlib import Path
from PySide6.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QPushButton,
    QLineEdit,
    QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator

class NumberSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.number = 0

        self.setObjectName("NumberSelector")

        self.load_stylesheet()

        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._decrement_button = QPushButton("-", self)
        self._decrement_button.setObjectName("Left")
        self._decrement_button.clicked.connect(self._decrement)
        layout.addWidget(self._decrement_button)

        self._number_label = QLineEdit(f"{self.number}", self)
        self._number_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._number_label.setMaximumHeight(self._decrement_button.sizeHint().height())
        self._number_label.setValidator(QIntValidator(self))
        layout.addWidget(self._number_label)

        self._increment_button = QPushButton("+", self)
        self._increment_button.setObjectName("Right")
        self._increment_button.clicked.connect(self._increment)
        layout.addWidget(self._increment_button)

    def _increment(self):
        self.number += 1
        self._number_label.setText(f"{self.number}")

    def _decrement(self):
        self.number -= 1
        self._number_label.setText(f"{self.number}")

    def load_stylesheet(self):
        styles_path = Path(__file__).parent / "number_selector.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())
