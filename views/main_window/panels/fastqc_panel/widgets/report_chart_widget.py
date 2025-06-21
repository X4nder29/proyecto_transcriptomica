from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QStyleOption,
    QStyle,
    QLabel,
)
from PySide6.QtGui import QPainter, QPixmap, QImage
from PySide6.QtCore import Qt, QFile, QTextStream


class ReportChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("ReportChartWidget")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

        self.chart = QLabel(self)
        self.chart.setObjectName("ReportChartWidgetChart")
        self.chart.setScaledContents(True)
        self.main_layout.addWidget(self.chart)

    def set_chart(self, chart_path: Path):
        self.chart.setPixmap(QPixmap.fromImage(QImage(str(chart_path))).scaledToHeight(self.parent().height(), Qt.TransformationMode.SmoothTransformation))

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()

    def paintEvent(self, _):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
