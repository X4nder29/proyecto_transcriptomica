from pathlib import Path
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QGuiApplication, QFontMetrics
from PySide6.QtCore import Qt, QFile, QTextStream
from views.widgets import ItemWidget, ItemActionWidget


class WorkspaceFileItemWidget(ItemWidget):
    def __init__(self, name: str, path: str, parent: QWidget = None):
        self.name = name
        self.path = path
        super().__init__(":/assets/file.svg", parent=parent)
        self.load_stylesheet(QGuiApplication.styleHints().colorScheme())
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)

    def setup_ui(self):
        super().setup_ui()

        self.setObjectName("WorkspaceFileItemWidget")

        self.name_label = QLabel(self.name, self.content_area)
        self.name_label.setObjectName("NameLabel")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.name_label.setText(
            QFontMetrics(self.name_label.font()).elidedText(
                str(self.name),
                Qt.TextElideMode.ElideRight,
                235,
            ),
        )
        self.content_area_layout.addWidget(self.name_label)

        self.path_label = QLabel(self.path, self.content_area)
        self.path_label.setObjectName("PathLabel")
        self.path_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.path_label.setText(
            QFontMetrics(self.path_label.font()).elidedText(
                str(self.path),
                Qt.TextElideMode.ElideRight,
                235,
            ),
        )
        self.content_area_layout.addWidget(self.path_label)

        self.open_action = ItemActionWidget(":/assets/folder.svg", self.action_area)
        self.open_action.setToolTip("Abrir carpeta de archivo")
        self.action_area_layout.addWidget(self.open_action)

        self.delete_action = ItemActionWidget(":/assets/trash.svg", self.action_area)
        self.delete_action.setToolTip("Eliminar archivo")
        self.action_area_layout.addWidget(self.delete_action)

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

    def _on_resize_finished(self):
        self.name_label.setText(
            QFontMetrics(self.name_label.font()).elidedText(
                str(self.name),
                Qt.TextElideMode.ElideRight,
                self.width() - 175,
            ),
        )
        self.path_label.setText(
            QFontMetrics(self.path_label.font()).elidedText(
                str(self.path),
                Qt.TextElideMode.ElideRight,
                self.width() - 175,
            ),
        )
