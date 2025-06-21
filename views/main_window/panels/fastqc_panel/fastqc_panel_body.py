from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QSizePolicy,
    QStackedWidget,
)
from PySide6.QtCore import QFile, QTextStream
from views.widgets import (
    SimpleInputFileWidget,
)
from .widgets import (
    SummaryListWidget,
    UnselectedReportWidget,
    ReportGenerationWidget,
    UnselectedReportVisualizationWidget,
    BasicStatisticsReportWidget,
    ReportChartWidget,
    ReportTableWidget,
)


class FastqcPanelBody(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("FastqcPanelBody")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)
        self.setLayout(self.main_layout)

        self.input_file_widget = SimpleInputFileWidget(self)
        self.main_layout.addWidget(self.input_file_widget, 0, 0, 1, 1)

        self.summary_list_widget = SummaryListWidget(self)
        self.main_layout.addWidget(self.summary_list_widget, 1, 0, 1, 1)

        self.basic_statistics_report_widget = BasicStatisticsReportWidget(self)
        self.basic_statistics_report_widget.setVisible(False)
        self.main_layout.addWidget(self.basic_statistics_report_widget, 0, 1, 1, 1)

        self.report_content_area = QStackedWidget(self)
        self.report_content_area.setObjectName("ReportContentArea")
        self.report_content_area.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        self.main_layout.addWidget(self.report_content_area, 0, 1, 3, 1)

        self.unselected_report_widget = UnselectedReportWidget(self)
        self.report_content_area.addWidget(self.unselected_report_widget)

        self.report_generation_widget = ReportGenerationWidget(self)
        self.report_content_area.addWidget(self.report_generation_widget)

        self.unselected_report_visualization_widget = (
            UnselectedReportVisualizationWidget(self)
        )
        self.report_content_area.addWidget(self.unselected_report_visualization_widget)

        self.report_chart_widget = ReportChartWidget(self)
        self.report_content_area.addWidget(self.report_chart_widget)

        self.report_table_widget = ReportTableWidget(self.report_content_area)
        self.report_content_area.addWidget(self.report_table_widget)

        self.main_layout.setColumnStretch(1, 2)
        self.main_layout.setRowStretch(2, 1)

        # body widgets setup can be added here

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
