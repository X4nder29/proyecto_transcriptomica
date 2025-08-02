from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtGui import QGuiApplication, QIcon, QFontMetrics
from PySide6.QtCore import Qt, QFile, QTextStream, QTimer


class SelectFilePushButton(QPushButton):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)
        self.load_stylesheet(QGuiApplication.styleHints().colorScheme())
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)

        self._resize_timer = QTimer()
        self._resize_timer.setSingleShot(True)
        self._resize_timer.timeout.connect(self._on_resize_finished)

    def setup_ui(self):
        self.setObjectName("SelectFilePushButton")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(60)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

        self.icon_label = QLabel(self)
        self.icon_label.setObjectName("IconLabel")
        self.icon_label.setPixmap(QIcon(":/assets/file.svg").pixmap(24, 24))
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.main_layout.addWidget(self.icon_label)

        self.label_area = QWidget(self)
        self.label_area.setObjectName("LabelArea")
        self.main_layout.addWidget(self.label_area)

        self.label_area_layout = QVBoxLayout(self.label_area)
        self.label_area_layout.setContentsMargins(0, 0, 0, 0)
        self.label_area_layout.setSpacing(0)
        self.label_area_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_area.setLayout(self.label_area_layout)

        self.primary_label = QLabel(self.label_area)
        self.primary_label.setObjectName("PrimaryLabel")
        self.primary_label.setText("Clic para seleccionar un archivo")
        self.primary_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label_area_layout.addWidget(self.primary_label)

    def set_file(self, name: str, path: str):
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setToolTip(path)
        self.icon_label.setPixmap(QIcon(":/assets/file.svg").pixmap(24, 24))

        self.primary_label.setText(
            QFontMetrics(self.primary_label.font()).elidedText(
                str(name),
                Qt.TextElideMode.ElideRight,
                self.width() - 60,
            )
        )
        self.primary_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def clear_file(self):
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setToolTip("")
        self.icon_label.setPixmap(QIcon(":/assets/upload_file.svg").pixmap(24, 24))

        self.primary_label.setText("Clic para seleccionar un archivo")
        self.primary_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

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
        self.primary_label.setText(
            QFontMetrics(self.primary_label.font()).elidedText(
                str(self.primary_label.text()),
                Qt.TextElideMode.ElideRight,
                self.width(),
            ),
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._resize_timer.start(50)

    def sizeHint(self):
        return self.layout().sizeHint()
