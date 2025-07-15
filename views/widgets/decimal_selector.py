from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSizePolicy,
    QStyle,
    QStyleOption,
    QDoubleSpinBox,
    QAbstractSpinBox,
    QToolButton,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QFile, QTextStream


class DecimalSelector(QWidget):
    def __init__(self, parent: QWidget = None, decimals: int = 1, step: float = 0.1):
        super().__init__(parent)
        self._decimals = decimals
        self._step = step
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("DecimalSelector")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        self._spin_box = QDoubleSpinBox(self)
        self._spin_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._spin_box.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self._spin_box.setDecimals(self._decimals)
        self._spin_box.setSingleStep(self._step)

        self._decrement_button = QToolButton(parent=self, text="-")
        self._decrement_button.setObjectName("DecrementButton")
        self._decrement_button.setFixedHeight(self._spin_box.sizeHint().height())
        self._decrement_button.clicked.connect(self._spin_box.stepDown)

        self._increment_button = QToolButton(parent=self, text="+")
        self._increment_button.setObjectName("IncrementButton")
        self._increment_button.setFixedHeight(self._spin_box.sizeHint().height())
        self._increment_button.clicked.connect(self._spin_box.stepUp)

        self.main_layout.addWidget(self._decrement_button)
        self.main_layout.addWidget(self._spin_box)
        self.main_layout.addWidget(self._increment_button)

    def value(self) -> float:
        return self._spin_box.value()

    def set_value(self, value: float):
        self._spin_box.setValue(value)

    def set_decimals(self, decimals: int):
        self._spin_box.setDecimals(decimals)

    def set_range(self, minimum: float, maximum: float):
        self._spin_box.setRange(minimum, maximum)

    def set_single_step(self, step: float):
        self._spin_box.setSingleStep(step)

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
        super().paintEvent(event)
