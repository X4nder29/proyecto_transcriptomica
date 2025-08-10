from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStyle,
    QStyleOption,
    QLabel,
    QLineEdit,
    QDialog,
    QDialogButtonBox,
    QPushButton,
    QSpacerItem,
)
from PySide6.QtGui import QGuiApplication, QPainter, QIcon
from PySide6.QtCore import Qt, QSize, QFile, QTextStream


class CreateWorkspaceDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_stylesheet(QGuiApplication.styleHints().colorScheme())
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)

    def setup_ui(self):
        self.setWindowTitle("Crear Workspace")
        self.setObjectName("CreateWorkspace")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 20, 40, 20)
        self.main_layout.setSpacing(20)

        # title
        self.title = QLabel("Crear Workspace")
        self.title.setObjectName("Title")
        self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.main_layout.addWidget(self.title)

        # name

        self.name_area = QWidget(self)
        self.name_area.setObjectName("NameArea")
        self.main_layout.addWidget(self.name_area)

        self.name_area_layout = QHBoxLayout(self.name_area)
        self.name_area_layout.setContentsMargins(0, 0, 0, 0)
        self.name_area_layout.setSpacing(13)

        self.name_label = QLabel("Nombre")
        self.name_label.setObjectName("NameLabel")
        self.name_label.setAlignment(Qt.AlignVCenter)
        self.name_label.setMinimumWidth(50)
        self.name_area_layout.addWidget(self.name_label)

        self.name_input = QLineEdit(self)
        self.name_input.setObjectName("NameInput")
        self.name_input.setPlaceholderText("Ingrese el nombre")
        self.name_input.setAlignment(Qt.AlignVCenter)
        self.name_input.setMinimumHeight(30)
        self.name_input.setMinimumWidth(200)
        self.name_input.textChanged.connect(self.validate_inputs)
        self.name_area_layout.addWidget(self.name_input)

        # save location

        self.location_area = QWidget(self)
        self.location_area.setObjectName("LocationArea")
        self.main_layout.addWidget(self.location_area)

        self.location_area_layout = QHBoxLayout(self.location_area)
        self.location_area_layout.setContentsMargins(0, 0, 0, 0)
        self.location_area_layout.setSpacing(0)

        self.location_label = QLabel("Ubicación")
        self.location_label.setObjectName("LocationLabel")
        self.location_label.setAlignment(Qt.AlignVCenter)
        self.location_label.setMinimumWidth(50)
        self.location_area_layout.addWidget(self.location_label)

        self.location_input = QLineEdit("", self)
        self.location_input.setObjectName("LocationInput")
        self.location_input.setPlaceholderText("Ingrese la ubicación")
        self.location_input.setMinimumHeight(30)
        self.location_input.setMinimumWidth(200)
        self.location_input.textChanged.connect(self.validate_inputs)
        self.location_area_layout.addWidget(self.location_input)

        self.location_area_layout.setSpacing(10)

        self.location_button = QPushButton(self)
        self.location_button.setObjectName("LocationButton")
        self.location_button.setIcon(QIcon(":/assets/folder.svg"))
        self.location_button.setIconSize(QSize(16, 16))
        self.location_button.setFixedSize(
            self.location_input.height(), self.location_input.height()
        )
        self.location_area_layout.addWidget(self.location_button)

        #

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.setObjectName("Buttons")
        self.buttons.button(QDialogButtonBox.Ok).setText("Ok")
        self.buttons.button(QDialogButtonBox.Cancel).setText("Cancelar")
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(False)

        self.main_layout.addWidget(self.buttons)

    def validate_inputs(self):
        name_filled = bool(self.name_input.text().strip())
        location_filled = bool(self.location_input.text().strip())

        all_filled = name_filled and location_filled
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(all_filled)

    def load_stylesheet(self, scheme: Qt.ColorScheme):
        qss_file = QFile(
            f":/styles/{Path(__file__).stem}_{"dark" if scheme == Qt.ColorScheme.Dark else "light"}.qss"
        )
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            style = self.style()
            style.unpolish(self)
            style.polish(self)
            self.update()
            qss_file.close()

    def paintEvent(self, _):
        option = QStyleOption()
        option.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)
