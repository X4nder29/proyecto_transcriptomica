from pathlib import Path
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QFontMetrics
from PySide6.QtCore import Qt, QFile, QTextStream
from views.widgets import ItemAbstractButton


class FileSelectorDialogItemWidget(ItemAbstractButton):

    def __init__(self, name: str, path: str, icon: str, parent: QWidget = None):
        self.name = name
        self.path = path
        super().__init__(icon, parent)
        self.load_stylesheet()

    def setup_ui(self):

        super().setup_ui()

        self.setObjectName("FileSelectorDialogItemWidget")
        self.setToolTip(self.path)

        self.name_label = QLabel(self.name, self.content_area)
        self.name_label.setObjectName("NameLabel")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.name_label.setText(
            QFontMetrics(self.name_label.font()).elidedText(
                str(self.name),
                Qt.TextElideMode.ElideRight,
                260,
            ),
        )
        self.content_area_layout.addWidget(self.name_label)

        self.path_label = QLabel(self.content_area)
        self.path_label.setObjectName("PathLabel")
        self.path_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.path_label.setText(
            QFontMetrics(self.path_label.font()).elidedText(
                str(self.path),
                Qt.TextElideMode.ElideRight,
                260,
            ),
        )
        self.content_area_layout.addWidget(self.path_label)

    def _on_resize_finished(self):
        self.path_label.setText(
            QFontMetrics(self.path_label.font()).elidedText(
                str(self.path),
                Qt.TextElideMode.ElideRight,
                self.width() - 100,
            ),
        )
        self.name_label.setText(
            QFontMetrics(self.name_label.font()).elidedText(
                str(self.name),
                Qt.TextElideMode.ElideRight,
                self.width() - 100,
            ),
        )

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
