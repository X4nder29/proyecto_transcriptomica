from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QPushButton,
    QStyleOption,
    QStyle,
    QLabel,
)


class SettingsPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("SettingsPanel")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setupUi()

    def setupUi(self):

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setStyleSheet(
            """
            QWidget#SettingsPanel {
                background-color: none;
            }
            """
        )

        self.QLabel = QLabel("Settings")
        self.main_layout.addWidget(self.QLabel)
