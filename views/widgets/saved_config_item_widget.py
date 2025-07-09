from pathlib import Path
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QFontMetrics
from PySide6.QtCore import Qt, QFile, QTextStream
from views.widgets import ItemWidget, ItemActionWidget


class SavedConfigItemWidget(ItemWidget):
    def __init__(self, name: str, parent: QWidget = None):
        self.name = name
        super().__init__(":/assets/file.svg", parent=parent)
        self.load_stylesheet()

    def setup_ui(self):
        super().setup_ui()

        self.setObjectName("SavegConfigItemWidget")

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

        self.load_action = ItemActionWidget(":/assets/load.svg", self.action_area)
        self.load_action.setToolTip("Cargar configuración guardada")
        self.action_area_layout.addWidget(self.load_action)

        self.delete_action = ItemActionWidget(":/assets/trash.svg", self.action_area)
        self.delete_action.setToolTip("Eliminar configuración guardada")
        self.action_area_layout.addWidget(self.delete_action)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def _on_resize_finished(self):
        self.name_label.setText(
            QFontMetrics(self.name_label.font()).elidedText(
                str(self.name),
                Qt.TextElideMode.ElideRight,
                self.width() - 175,
            ),
        )
