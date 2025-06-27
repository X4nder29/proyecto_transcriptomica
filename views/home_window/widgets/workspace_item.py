import textwrap
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QMenu,
    QStyleOption,
    QStyle,
)
from PySide6.QtGui import QPixmap, QIcon, QPainter, QAction
from PySide6.QtCore import Qt, Signal, QFile, QTextStream


class WorkspaceItem(QWidget):
    clicked = Signal()

    def __init__(self, name: str, path: Path, parent=None):
        super().__init__(parent=parent)

        self.name = name
        self.path = path
        self.enable = self.path.exists() and self.path.is_dir()

        self.setObjectName("WorkspaceItem")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(64)
        """ self.setEnabled(self.path.exists() and self.path.is_dir()) """

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # Icono (Etiqueta con imagen)

        icon_label = QLabel(self)
        icon_label.setObjectName("IconLabel")
        icon_label.setEnabled(self.enable)
        icon_label.setFixedSize(32, 32)
        icon_label.setPixmap(
            QPixmap(":/assets/adn.svg").scaled(
                24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignTop)

        ## Contenedor del texto

        content = QWidget(self)
        content.setObjectName("Content")
        self.main_layout.addWidget(content)

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Nombre del archivo
        file_name_label = QLabel(self.name)
        file_name_label.setObjectName("FileNameLabel")
        file_name_label.setEnabled(self.enable)
        content_layout.addWidget(file_name_label, alignment=Qt.AlignmentFlag.AlignTop)

        # Ruta del archivo
        file_path_label = QLabel(
            textwrap.shorten(str(self.path), width=100, placeholder="...")
        )
        file_path_label.setObjectName("FilePathLabel")
        file_path_label.setEnabled(self.enable)
        content_layout.addWidget(file_path_label, alignment=Qt.AlignmentFlag.AlignTop)

        content_layout.addStretch(1)

        ## Action button

        self.action_button = QPushButton(self)
        self.action_button.setObjectName("ActionButton")
        self.action_button.setFixedSize(30, 30)
        self.action_button.setIcon(QIcon(":/assets/more_vert.svg"))
        self.main_layout.addWidget(self.action_button)

        self.menu = QMenu(self)
        self.menu.setObjectName("Menu")
        self.menu.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.delete_action = QAction("Eliminar", self.menu)
        self.menu.addAction(self.delete_action)

        self.action_button.clicked.connect(self.show_menu)

    def show_menu(self):
        print("Show menu")
        self.menu.exec_(
            self.action_button.mapToGlobal(self.action_button.rect().bottomLeft())
        )

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def mousePressEvent(self, _):
        if self.enable:
            self.clicked.emit()
            print("Clicked")

    def paintEvent(self, _):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
