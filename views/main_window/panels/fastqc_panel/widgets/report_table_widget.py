from pathlib import Path
from PySide6.QtWidgets import QSizePolicy, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt, QFile, QTextStream


class ReportTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("ReportTableWidget")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("ReportTable")
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(
            ["Sequence", "Count", "Percentage", "Possible Source"]
        )
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.verticalHeader().setVisible(False)

        self.header = self.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

    def set_table_data(self, data: list[tuple[str, int, int, str]]):
        self.setRowCount(len(data))
        for row, (sequence, count, percentage, source) in enumerate(data):
            self.setItem(row, 0, QTableWidgetItem(sequence))
            self.setItem(row, 1, QTableWidgetItem(str(count)))
            self.setItem(row, 2, QTableWidgetItem(str(percentage)))
            self.setItem(row, 3, QTableWidgetItem(source))

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
