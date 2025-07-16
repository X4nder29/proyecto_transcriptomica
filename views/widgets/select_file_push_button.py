from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtGui import QIcon, QFontMetrics
from PySide6.QtCore import Qt, QFile, QTextStream, QTimer


class SelectFilePushButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName("SelectFilePushButton")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(60)

        self.load_stylesheet()
        self.setup_ui()

        self._resize_timer = QTimer()
        self._resize_timer.setSingleShot(True)
        self._resize_timer.timeout.connect(self._on_resize_finished)

    def setup_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

        self.icon_label = QLabel(self)
        self.icon_label.setObjectName("IconLabel")
        self.icon_label.setPixmap(QIcon(":/assets/upload_file.svg").pixmap(24, 24))
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.main_layout.addWidget(self.icon_label)

        self.label_area = QWidget(self)
        self.label_area.setObjectName("LabelArea")
        self.main_layout.addWidget(self.label_area)

        self.label_area_layout = QVBoxLayout(self.label_area)
        self.label_area_layout.setContentsMargins(0, 0, 0, 0)
        self.label_area_layout.setSpacing(0)
        self.label_area_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label_area.setLayout(self.label_area_layout)

        self.primary_label = QLabel(self.label_area)
        self.primary_label.setObjectName("PrimaryLabel")
        self.primary_label.setText("Arrastrar y soltar un archivo aquí")
        self.primary_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label_area_layout.addWidget(self.primary_label)

        self.secondary_label = QLabel(self.label_area)
        self.secondary_label.setObjectName("SecondaryLabel")
        self.secondary_label.setText("O hacer clic para seleccionar un archivo")
        self.secondary_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label_area_layout.addWidget(self.secondary_label)

    def set_file(self, name: str, path: str):
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setToolTip(path)
        self.icon_label.setPixmap(QIcon(":/assets/file.svg").pixmap(24, 24))

        self.primary_label.setText(name)
        self.primary_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.secondary_label.setText(
            QFontMetrics(self.secondary_label.font()).elidedText(
                str(path),
                Qt.TextElideMode.ElideRight,
                self.width() - 60,
            )
        )
        self.secondary_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def clear_file(self):
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setToolTip("")
        self.icon_label.setPixmap(QIcon(":/assets/upload_file.svg").pixmap(24, 24))

        self.primary_label.setText("Arrastrar y soltar un archivo aquí")
        self.primary_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.secondary_label.setText("O hacer clic para seleccionar un archivo")
        self.secondary_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def _on_resize_finished(self):
        self.primary_label.setText(
            QFontMetrics(self.primary_label.font()).elidedText(
                str(self.primary_label.text()),
                Qt.TextElideMode.ElideRight,
                self.width(),
            ),
        )
        self.secondary_label.setText(
            QFontMetrics(self.secondary_label.font()).elidedText(
                self.secondary_label.text(),
                Qt.TextElideMode.ElideRight,
                self.width() - 50,  # Adjusted to account for icon width and padding
            ),
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._resize_timer.start(50)

    def sizeHint(self):
        return self.layout().sizeHint()
