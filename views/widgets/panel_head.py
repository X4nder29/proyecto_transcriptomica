from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QProgressBar,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QFile, QTextStream


class PanelHead(QWidget):

    def __init__(self, title, parent=None):
        super().__init__(parent=parent)

        self.title = title

        self.setObjectName("PanelHead")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)
        self.setLayout(self.main_layout)

        # title label

        self.title = QLabel(self.title, self)
        self.title.setObjectName("title")
        self.main_layout.addWidget(self.title)

        # add stretch

        self.main_layout.addStretch()

        # inderteminate progress bar
        self.indeterminate_progress_bar_background = QWidget(self)
        self.indeterminate_progress_bar_background.setObjectName("IndeterminateProgressBarBackground")
        self.indeterminate_progress_bar_background.setFixedWidth(150)
        self.indeterminate_progress_bar_background.setVisible(False)
        self.main_layout.addWidget(self.indeterminate_progress_bar_background)

        self.indeterminate_progress_bar_background_layout = QHBoxLayout(self.indeterminate_progress_bar_background)
        self.indeterminate_progress_bar_background_layout.setContentsMargins(15, 0, 15, 0)
        self.indeterminate_progress_bar_background_layout.setSpacing(0)
        self.indeterminate_progress_bar_background.setLayout(self.indeterminate_progress_bar_background_layout)

        self.indeterminate_progress_bar = QProgressBar(self)
        self.indeterminate_progress_bar.setObjectName("IndeterminateProgressBar")
        self.indeterminate_progress_bar.setRange(0, 0)
        self.indeterminate_progress_bar.setToolTip("Ejecución en curso")
        self.indeterminate_progress_bar.setTextVisible(False)
        self.indeterminate_progress_bar_background_layout.addWidget(
            self.indeterminate_progress_bar
        )

        # cancel button
        self.cancel_button = QPushButton(self)
        self.cancel_button.setObjectName("ActionButton")
        self.cancel_button.setToolTip("Cancelar ejecución")
        self.cancel_button.setIcon(QIcon(":/assets/cancel.svg"))
        self.cancel_button.setVisible(False)
        self.main_layout.addWidget(self.cancel_button)

        # play button

        self.play_button = QPushButton(self)
        self.play_button.setObjectName("ActionButton")
        self.play_button.setToolTip("Ejecutar")

        self.play_button_icon = QIcon(":/assets/play.svg")
        self.play_button.setIcon(self.play_button_icon)

        self.main_layout.addWidget(self.play_button)

        # star button

        self.star_button = QPushButton(self)
        self.star_button.setObjectName("ActionButton")
        self.star_button.setToolTip("Marcar como favorito configuración actual")

        self.star_button_icon = QIcon(":/assets/filled_star.svg")
        self.star_button.setIcon(self.star_button_icon)

        self.main_layout.addWidget(self.star_button)

        # cli push button

        self.cli_push_button = QPushButton(self)
        self.cli_push_button.setObjectName("ActionButton")
        self.cli_push_button.setIcon(QIcon(":/assets/cli_filled.svg"))
        self.cli_push_button.setToolTip("Visualizar comando a ejecutar")
        self.main_layout.addWidget(self.cli_push_button)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
