from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSizePolicy,
    QLabel,
    QPushButton,
    QButtonGroup,
)
from PySide6.QtCore import Qt


class ModeArea(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("ModeArea")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        self.mode_label = QLabel("Modo de\n Operación", self)
        self.mode_label.setObjectName("ModeLabel")
        self.mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        self.pe_button = QPushButton(self)
        self.pe_button.setObjectName("ModeButton")
        self.pe_button.setText("PE")
        self.pe_button.setToolTip("Paired End")
        self.pe_button.setCheckable(True)
        self.button_group.addButton(self.pe_button)
        self.button_group.setId(self.pe_button, 1)

        self.se_button = QPushButton(self)
        self.se_button.setObjectName("ModeButton")
        self.se_button.setText("SE")
        self.se_button.setToolTip("Single End")
        self.se_button.setCheckable(True)
        self.se_button.setChecked(True)
        self.button_group.addButton(self.se_button)
        self.button_group.setId(self.se_button, 0)

        self.main_layout.addWidget(self.mode_label)
        self.main_layout.addWidget(self.pe_button)
        self.main_layout.addWidget(self.se_button)
