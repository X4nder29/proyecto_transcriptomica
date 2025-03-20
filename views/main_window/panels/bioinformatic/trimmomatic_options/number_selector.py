from PySide6.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
)
from PySide6.QtCore import Qt

class NumberSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.number = 0
        self.setStyleSheet(
            """
            background-color: #555;
            padding: 1em;
            """
        )
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._decrement_button = QPushButton("-", self)
        self._decrement_button.setStyleSheet(
            """
            QPushButton {
                background-color: #555;
                padding: 0.5em;
                color: white;
                border: none;
                border-top-left-radius: 0.5em;
                border-bottom-left-radius: 0.5em;
            }

            QPushButton:hover {
                background-color: #666;
            }
            """
        )
        self._decrement_button.clicked.connect(self._decrement)
        layout.addWidget(self._decrement_button)

        self._number_label = QLabel(f"{self.number}", self)
        self._number_label.setStyleSheet(
            """
            color: white;
            padding: 0em;
            text-align: center;
            """
        )
        self._number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._number_label.setMaximumHeight(self._decrement_button.sizeHint().height())
        layout.addWidget(self._number_label)

        self._increment_button = QPushButton("+", self)
        self._increment_button.setStyleSheet(
            """
            QPushButton {
                background-color: #555;
                padding: 0.5em;
                color: white;
                border: none;
                border-top-right-radius: 0.5em;
                border-bottom-right-radius: 0.5em;
            }

            QPushButton:hover {
                background-color: #666;
            }
            """
        )
        self._increment_button.clicked.connect(self._increment)
        layout.addWidget(self._increment_button)

    def _increment(self):
        self.number += 1
        self._number_label.setText(f"{self.number}")

    def _decrement(self):
        self.number -= 1
        self._number_label.setText(f"{self.number}")
