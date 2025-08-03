from pathlib import Path
from typing import Optional, Tuple
from PySide6.QtWidgets import (
    QWidget,
    QStyleOption,
    QStyle,
    QSizePolicy,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
)
from PySide6.QtGui import QGuiApplication, QPainter, QIcon
from PySide6.QtCore import Qt, QFile, QTextStream


class ComboBoxSuboptionWidget(QWidget):

    def __init__(
        self,
        title: str,
        parent: QWidget = None,
        checkable: bool = False,
        options: Optional[list[Tuple[str, Optional[str]]]] = None,
    ):
        super().__init__(parent)
        self.title = title
        self.options = options
        self.checkable = checkable
        self.load_stylesheet(QGuiApplication.styleHints().colorScheme())
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)

    def setup_ui(self):
        self.setObjectName("ComboBoxSubOptionWidget")

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        # checkbox
        if self.checkable:
            self.checkbox = QPushButton(self)
            self.checkbox.setObjectName("Checkbox")
            self.checkbox.setCheckable(True)
            self.checkbox.setChecked(False)
            self.checkbox.setIcon(QIcon(":/assets/checkbox_outlined.svg"))
            self.checkbox.toggled.connect(self._toggle_checkbox_icon)
            self.main_layout.addWidget(
                self.checkbox, alignment=Qt.AlignmentFlag.AlignLeft
            )

        # label
        self.label = QLabel(self.title, self)
        self.label.setObjectName("SubOptionWidgetLabel")
        self.label.setToolTip("Enable or disable this option")
        self.main_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft)

        # spacer
        self.main_layout.addStretch(1)

        # combo box

        self.combo_box = QComboBox(self)
        self.combo_box.setObjectName("ComboBox")
        self.combo_box.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        if self.options is not None:
            for option, data in self.options:
                if data is None:
                    self.combo_box.addItem(option)
                else:
                    self.combo_box.addItem(option, data)
        self.combo_box.setCurrentIndex(0)
        self.main_layout.addWidget(
            self.combo_box, alignment=Qt.AlignmentFlag.AlignRight
        )

    def _toggle_checkbox_icon(self):
        if self.checkbox.isChecked():
            self.checkbox.setIcon(QIcon(":/assets/checkbox_filled.svg"))
        else:
            self.checkbox.setIcon(QIcon(":/assets/checkbox_outlined.svg"))

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
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
        super().paintEvent(_)
