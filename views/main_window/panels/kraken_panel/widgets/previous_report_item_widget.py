from pathlib import Path
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QFontMetrics
from PySide6.QtCore import Qt, QFile, QTextStream, Signal
from views.widgets import ItemWidget, ItemActionWidget


class PreviousReportItemWidget(ItemWidget):
    clicked = Signal()

    def __init__(self, name: str, path: str, parent: QWidget = None):
        self.name = name
        self.path = path
        super().__init__(":/assets/file.svg", parent=parent)
        self.load_stylesheet()

    def setup_ui(self):
        super().setup_ui()

        self.setObjectName("PreviousReportItemWidget")

        self.name_label = QLabel(self.name, self.content_area)
        self.name_label.setObjectName("NameLabel")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.name_label.setText(
            QFontMetrics(self.name_label.font()).elidedText(
                str(self.name),
                Qt.TextElideMode.ElideRight,
                200,
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
                200,
            ),
        )
        self.content_area_layout.addWidget(self.path_label)

        self.open_action = ItemActionWidget(":/assets/folder.svg", self.action_area)
        self.open_action.setToolTip("Abrir carpeta de reporte")
        self.action_area_layout.addWidget(self.open_action)

        self.delete_action = ItemActionWidget(":/assets/trash.svg", self.action_area)
        self.delete_action.setToolTip("Eliminar reporte")
        self.action_area_layout.addWidget(self.delete_action)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
