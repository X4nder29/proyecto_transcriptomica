from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QSizePolicy,
    QPushButton,
    QButtonGroup,
    QStyleOption,
    QStyle,
)
from PySide6.QtGui import QPainter, QIcon, Qt
from PySide6.QtCore import QSize
from pathlib import Path


class MainWindowSideBar(QWidget):

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(parent)

        self.setObjectName("SideBar")
        self.setFixedWidth(68)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.sections = [
            "home",
            "trimmomatic",
            "sortmerna",
            "kraken",
            "fastqc",
        ]
        self.outlined_icon = [
            QIcon("assets/home_outlined.svg"),
            QIcon("assets/adn_outlined.svg"),
            QIcon("assets/cut_outlined.svg"),
            QIcon("assets/kraken_outlined.svg"),
            QIcon("assets/graphics_outlined.svg"),
        ]
        self.filled_icon = [
            QIcon("assets/home.svg"),
            QIcon("assets/adn.svg"),
            QIcon("assets/cut.svg"),
            QIcon("assets/kraken.svg"),
            QIcon("assets/graphics.svg"),
        ]
        self.buttons = []

        # icon app

        self.icon_app = QLabel()
        self.icon_app.setFixedHeight(44)
        self.icon_app.setToolTip("TranscriptoHub")

        self.icon_app.setPixmap(QIcon("assets/icon.svg").pixmap(QSize(32, 32)))
        self.icon_app.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.icon_app, alignment=Qt.AlignmentFlag.AlignTop)
        self.main_layout.addStretch()

        # button group

        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        self.button_group.buttonClicked.connect(
            lambda btn: self.changeButtonIcon(btn)
        )

        # home section

        self.home_button = QPushButton()
        self.home_button.setFixedHeight(44)
        self.home_button.setToolTip("Inicio")
        self.home_button.setCheckable(True)
        self.home_button.setChecked(True)
        self.home_button.setIcon(self.filled_icon[0])
        self.home_button.setIconSize(QSize(24, 24))

        self.button_group.addButton(self.home_button, 0)
        self.main_layout.addWidget(
            self.home_button, alignment=Qt.AlignmentFlag.AlignTop
        )

        # trimmomatic section

        self.trimmomatic_button = QPushButton()
        self.trimmomatic_button.setFixedHeight(44)
        self.trimmomatic_button.setToolTip("Trimmomatic")
        self.trimmomatic_button.setCheckable(True)
        self.trimmomatic_button.setIcon(self.outlined_icon[1])
        self.trimmomatic_button.setIconSize(QSize(26, 26))

        self.button_group.addButton(self.trimmomatic_button, 1)
        self.main_layout.addWidget(
            self.trimmomatic_button, alignment=Qt.AlignmentFlag.AlignTop
        )

        # sortmerna section

        self.sortmerna_button = QPushButton()
        self.sortmerna_button.setFixedHeight(44)
        self.sortmerna_button.setToolTip("Sortmerna")
        self.sortmerna_button.setCheckable(True)
        self.sortmerna_button.setIcon(self.outlined_icon[2])
        self.sortmerna_button.setIconSize(QSize(24, 24))

        self.button_group.addButton(self.sortmerna_button, 2)
        self.main_layout.addWidget(
            self.sortmerna_button, alignment=Qt.AlignmentFlag.AlignTop
        )

        # kraken section

        self.kraken_button = QPushButton()
        self.kraken_button.setFixedHeight(44)
        self.kraken_button.setToolTip("Kraken")
        self.kraken_button.setCheckable(True)
        self.kraken_button.setIcon(self.outlined_icon[3])
        self.kraken_button.setIconSize(QSize(24, 24))

        self.button_group.addButton(self.kraken_button, 3)
        self.main_layout.addWidget(
            self.kraken_button, alignment=Qt.AlignmentFlag.AlignTop
        )

        # fastqc section

        self.fastqc_button = QPushButton()
        self.fastqc_button.setFixedHeight(44)
        self.fastqc_button.setToolTip("FastQC")
        self.fastqc_button.setCheckable(True)
        self.fastqc_button.setIcon(self.outlined_icon[4])
        self.fastqc_button.setIconSize(QSize(24, 24))

        self.button_group.addButton(self.fastqc_button, 4)
        self.main_layout.addWidget(
            self.fastqc_button, alignment=Qt.AlignmentFlag.AlignTop
        )

        # settings section

        self.settings_button = QPushButton()
        self.settings_button.setFixedHeight(44)
        self.settings_button.setToolTip("Configuración")
        self.settings_button.setCheckable(True)
        self.button_group.addButton(self.settings_button, 5)

        self.settings_button_icon = QIcon("assets/settings_outlined.svg")
        self.settings_button.setIcon(self.settings_button_icon)
        self.settings_button.setIconSize(QSize(24, 24))
        self.main_layout.addStretch()
        self.main_layout.addWidget(
            self.settings_button, alignment=Qt.AlignmentFlag.AlignBottom
        )

    def changeButtonIcon(self, button):
        if button == self.home_button:
            self.home_button.setIcon(self.filled_icon[0])
        else:
            self.home_button.setIcon(self.outlined_icon[0])

        if button == self.trimmomatic_button:
            self.trimmomatic_button.setIcon(self.filled_icon[1])
        else:
            self.trimmomatic_button.setIcon(self.outlined_icon[1])

        if button == self.sortmerna_button:
            self.sortmerna_button.setIcon(self.filled_icon[2])
        else:
            self.sortmerna_button.setIcon(self.outlined_icon[2])

        if button == self.kraken_button:
            self.kraken_button.setIcon(self.filled_icon[3])
        else:
            self.kraken_button.setIcon(self.outlined_icon[3])

        if button == self.fastqc_button:
            self.fastqc_button.setIcon(self.filled_icon[4])
        else:
            self.fastqc_button.setIcon(self.outlined_icon[4])

    def load_stylesheet(self):
        styles_path = Path(__file__).parent / "main_window_sidebar.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
