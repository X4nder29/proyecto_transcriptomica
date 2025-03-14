import os
import textwrap
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QMenu,
    QStyleOption,
    QStyle
)
from PySide6.QtGui import QPixmap, QIcon, QPainter
from PySide6.QtCore import Qt, Signal


class FileWidget(QWidget):
    clicked = Signal()

    def __init__(self, file_path):
        super().__init__()

        self.file_path = file_path

        self.setupUi()

    def setupUi(self):

        self.setObjectName("file_widget")
        self.setStyleSheet(
            """

            QWidget#file_widget:hover {
                background-color: #303030;
            }

            """
        )
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(64)

        layout = QHBoxLayout(self)

        # Icono (Etiqueta con imagen)

        icon_label = QLabel(self)
        icon_label.setObjectName("icon_label")
        icon_label.setFixedSize(40, 40)
        icon_label.setPixmap(
            QPixmap("assets/adn.svg").scaled(
                24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        icon_label.setStyleSheet(
            """
            QLabel#icon_label {
                background-color: #FF6565;
                padding: 8px;
                border-radius: 8px;
            }
            """
        )

        # Contenedor del texto

        content = QWidget(self)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Nombre del archivo
        file_name_label = QLabel(os.path.basename(self.file_path))
        file_name_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: white;"
        )

        # Ruta del archivo
        file_path_label = QLabel(textwrap.shorten(self.file_path, width=100, placeholder="..."))
        file_path_label.setStyleSheet("font-size: 12px; color: #AAA;")

        # Botón de acción (tres puntos)
        self.action_button = QPushButton(self)
        self.action_button.setObjectName("action_button")
        self.action_button.setFixedSize(30, 30)
        self.action_button.setIcon(QIcon("assets/more_vert.svg"))
        self.action_button.setStyleSheet(
            """
            QPushButton#action_button {
                background-color: transparent;
                border-radius: none;
            }

            QPushButton#action_button:hover {
                background-color: #303030;
                border-radius: 8px;
            }
            """
        )

        self.menu = QMenu(self)
        self.menu.addAction("Eliminar")

        self.action_button.clicked.connect(self.showMenu)

        # Agregar widgets al layout del contenido
        content_layout.addWidget(file_name_label)
        content_layout.addWidget(file_path_label)

        # Agregar elementos al layout principal
        layout.addWidget(icon_label)
        layout.addWidget(content)
        layout.addWidget(self.action_button)

    def mousePressEvent(self, event):
        self.clicked.emit()
        print("Clicked")

    def showMenu(self):
        print("Show menu")
        self.menu.exec_(
            self.action_button.mapToGlobal(self.action_button.rect().bottomLeft())
        )

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
