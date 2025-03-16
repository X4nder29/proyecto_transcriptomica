from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QPushButton,
    QStyleOption,
    QStyle,
    QLabel,
)


class BioinformaticPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("BioinformaticPanel")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        self.setupUi()

    def setupUi(self):

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.setStyleSheet(
            """
            QWidget#BioinformaticPanel {
                background-color: #303030;
                }
            """
        )

        self.QLabel = QLabel("Bioinformatic Panel")

        self.main_layout.addWidget(self.QLabel)