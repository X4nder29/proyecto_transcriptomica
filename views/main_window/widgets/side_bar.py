from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QPushButton,
    QStyleOption,
    QStyle,
    QMenu,
)
from PySide6.QtGui import QPainter, QIcon, Qt
from PySide6.QtCore import QSize


class SideBar(QWidget):

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(parent)

        self.setObjectName("SideBar")
        self.setFixedWidth(68)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        self.setupUi()

    def setupUi(self):

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.setStyleSheet(
            """
            QWidget#SideBar {
                background-color: #303030;
            }
            """
        )

        # icon app

        self.icon_app_button = QPushButton()
        self.icon_app_button.setFixedHeight(44)
        self.icon_app_button.setStyleSheet(
            """
                QPushButton {
                    background-color: none;
                    border: none;
                    padding: 10px;
                }

                QPushButton:hover {
                    padding: 10px;
                    background-color: #505050;
                    border-radius: 10px;
                }

                QPushButton::menu-indicator {
                    image: none;
                    width: 0px;
                }
            """
        )
        self.icon_app_button.setToolTip("TranscriptoHub")

        self.icon_app_icon = QIcon("assets/icon.svg")
        self.icon_app_button.setIcon(self.icon_app_icon)
        self.icon_app_button.setIconSize(QSize(28, 28))

        menu = QMenu(self)
        menu.setStyleSheet(
            """
            QMenu {
                background-color: #505050; /* Color de fondo */
                border: 1px solid #303030; /* Borde opcional */
            }
            QMenu::item {
                padding: 6px 12px; /* Espaciado interno */
                color: white; /* Color del texto */
            }
            QMenu::item:selected { 
                background-color: #707070; /* Color cuando se selecciona */
            }
        """
        )

        open_file_option = menu.addAction("Abrir archivo")

        close_file_option = menu.addAction("Cerrar archivo")
        close_file_option.triggered.connect(self.closeFile)

        recent_file_option = menu.addAction("Archivo reciente")

        self.icon_app_button.setMenu(menu)

        # home section

        self.home_button = QPushButton()
        self.home_button.setFixedHeight(44)
        self.home_button.setStyleSheet(
            """
            QPushButton {
                    background-color: #222222;
                    border-radius: 10px;
            }
            """
        )
        self.home_button.setToolTip("Inicio")

        self.home_button_icon = QIcon("assets/home.svg")
        self.home_button.setIcon(self.home_button_icon)
        self.home_button.setIconSize(QSize(24, 24))

        # bioinformatics section

        self.bioinformatics_button = QPushButton()
        self.bioinformatics_button.setFixedHeight(44)
        self.bioinformatics_button.setStyleSheet(
            """
                QPushButton {
                    background-color: none;
                    border: none;
                    padding: 10px;
                }

                QPushButton:hover {
                    padding: 10px;
                    background-color: #505050;
                    border-radius: 10px;
                }
            """
        )
        self.bioinformatics_button.setToolTip("Bioinformática")

        self.bioinformatics_button_icon = QIcon("assets/adn_outlined.svg")
        self.bioinformatics_button.setIcon(self.bioinformatics_button_icon)
        self.bioinformatics_button.setIconSize(QSize(32, 32))

        # graphics section

        self.graphics_button = QPushButton()
        self.graphics_button.setFixedHeight(44)
        self.graphics_button.setStyleSheet(
            """
                QPushButton {
                    background-color: none;
                    border: none;
                    padding: 10px;
                }

                QPushButton:hover {
                    padding: 10px;
                    background-color: #505050;
                    border-radius: 10px;
                }
            """
        )
        self.graphics_button.setToolTip("FastQC")

        self.graphics_button_icon = QIcon("assets/graphics_outlined.svg")
        self.graphics_button.setIcon(self.graphics_button_icon)
        self.graphics_button.setIconSize(QSize(24, 24))

        # settings section

        self.settings_button = QPushButton()
        self.settings_button.setFixedHeight(44)
        self.settings_button.setStyleSheet(
            """
                QPushButton {
                    background-color: none;
                    border: none;
                }

                QPushButton:hover {
                    background-color: #505050;
                    border-radius: 10px;
                }
            """
        )
        self.settings_button.setToolTip("Configuración")

        self.settings_button_icon = QIcon("assets/settings_outlined.svg")
        self.settings_button.setIcon(self.settings_button_icon)
        self.settings_button.setIconSize(QSize(24, 24))

        # add widgets to layout

        self.main_layout.addWidget(
            self.icon_app_button, alignment=Qt.AlignmentFlag.AlignTop
        )
        self.main_layout.addStretch()
        self.main_layout.addWidget(
            self.home_button, alignment=Qt.AlignmentFlag.AlignTop
        )
        self.main_layout.addWidget(
            self.bioinformatics_button, alignment=Qt.AlignmentFlag.AlignTop
        )
        self.main_layout.addWidget(
            self.graphics_button, alignment=Qt.AlignmentFlag.AlignTop
        )
        self.main_layout.addStretch()
        self.main_layout.addWidget(
            self.settings_button, alignment=Qt.AlignmentFlag.AlignBottom
        )

    def changeButtonsStyle(self, index):
        buttons = [
            self.home_button,
            self.bioinformatics_button,
            self.graphics_button,
            self.settings_button,
        ]

        outlined_button_icons = [
            QIcon("assets/home_outlined.svg"),
            QIcon("assets/adn_outlined.svg"),
            QIcon("assets/graphics_outlined.svg"),
            QIcon("assets/settings_outlined.svg"),
        ]

        filled_button_icons = [
            QIcon("assets/home.svg"),
            QIcon("assets/adn.svg"),
            QIcon("assets/graphics.svg"),
            QIcon("assets/settings.svg"),
        ]

        for i, button in enumerate(buttons):
            if i == index:
                button.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #222222;
                        border-radius: 10px;
                    }
                    """
                )
                button.setIcon(filled_button_icons[i])
            else:
                button.setStyleSheet(
                    """
                    QPushButton {
                        background-color: none;
                        border: none;
                    }

                    QPushButton:hover {
                        background-color: #505050;
                        border-radius: 10px;
                    }
                    """
                )
                button.setIcon(outlined_button_icons[i])

    def openFile(self):
        pass

    def closeFile(self):
        self.window().close()
        from views.home_window import HomeWindow
        HomeWindow().show()

    def recentFile(self):
        pass

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
