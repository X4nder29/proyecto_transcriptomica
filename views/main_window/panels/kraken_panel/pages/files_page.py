from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStyleOption,
    QStyle,
    QSizePolicy,
    QLabel,
    QPushButton,
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QFile, QTextStream
from views.widgets import OperationModeWidget, SelectFilePushButton, ListWidget


class FilesPage(QWidget):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.load_stylesheet()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("UploadFilesPageWidget")

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)
        self.setLayout(self.main_layout)

        # upload container

        self.upload_container_widget = QWidget(self)
        self.upload_container_widget.setObjectName("UploadContainerWidget")
        self.main_layout.addWidget(self.upload_container_widget, 2)

        self.upload_container_layout = QVBoxLayout(self.upload_container_widget)
        self.upload_container_layout.setContentsMargins(0, 0, 0, 0)
        self.upload_container_layout.setSpacing(20)
        self.upload_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upload_container_widget.setLayout(self.upload_container_layout)

        self.operation_mode_widget = OperationModeWidget(self)
        self.operation_mode_widget.setMaximumWidth(600)
        self.operation_mode_widget.button_group.buttonClicked.connect(
            lambda button: self.change_operation_mode(button.text())
        )
        self.upload_container_layout.addWidget(self.operation_mode_widget)

        # select input files

        self.select_input_files_widget = QWidget(self)
        self.select_input_files_widget.setObjectName("SelectInputFilesWidget")
        self.select_input_files_widget.setMaximumWidth(600)
        self.select_input_files_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.upload_container_layout.addWidget(self.select_input_files_widget)

        self.select_input_files_layout = QHBoxLayout(self.select_input_files_widget)
        self.select_input_files_layout.setContentsMargins(0, 0, 0, 0)
        self.select_input_files_layout.setSpacing(10)
        self.select_input_files_widget.setLayout(self.select_input_files_layout)

        # select input file 1

        self.select_input_1_widget = QWidget(self.select_input_files_widget)
        self.select_input_1_widget.setObjectName("SelectInputsWidget")
        self.select_input_files_layout.addWidget(self.select_input_1_widget, 1)

        self.select_input_1_layout = QHBoxLayout(self.select_input_1_widget)
        self.select_input_1_layout.setContentsMargins(2, 2, 2, 2)
        self.select_input_1_layout.setSpacing(0)
        self.select_input_1_widget.setLayout(self.select_input_1_layout)

        self.select_file_1 = SelectFilePushButton(self.select_input_1_widget)
        self.select_input_1_layout.addWidget(self.select_file_1)

        # select input file 2

        self.select_input_2_widget = QWidget(self.select_input_files_widget)
        self.select_input_2_widget.setObjectName("SelectInputsWidget")
        self.select_input_2_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.select_input_2_widget.setVisible(False)
        self.select_input_files_layout.addWidget(self.select_input_2_widget, 1)

        self.select_input_2_layout = QHBoxLayout(self.select_input_2_widget)
        self.select_input_2_layout.setContentsMargins(2, 2, 2, 2)
        self.select_input_2_layout.setSpacing(0)
        self.select_input_2_widget.setLayout(self.select_input_2_layout)

        self.select_file_2 = SelectFilePushButton(self.select_input_2_widget)
        self.select_input_2_layout.addWidget(self.select_file_2)

        # select database

        self.select_database_label = QLabel("Seleccionar base de datos", self)
        self.select_database_label.setObjectName("SelectDatabaseLabel")
        self.select_database_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upload_container_layout.addWidget(self.select_database_label)

        self.select_database_widget = QWidget(self)
        self.select_database_widget.setObjectName("SelectDatabaseWidget")
        self.select_database_widget.setMaximumWidth(600)
        self.select_database_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.upload_container_layout.addWidget(self.select_database_widget)

        self.select_database_layout = QHBoxLayout(self.select_database_widget)
        self.select_database_layout.setContentsMargins(2, 2, 2, 2)
        self.select_database_layout.setSpacing(0)
        self.select_database_widget.setLayout(self.select_database_layout)

        self.select_database_button = SelectFilePushButton(self.select_database_widget)
        self.select_database_layout.addWidget(self.select_database_button)

        # Next page button
        self.next_page_button = QPushButton("Siguiente", self)
        self.next_page_button.setObjectName("NavigationButton")
        self.next_page_button.setMinimumWidth(200)
        self.next_page_button.setMinimumHeight(50)
        self.upload_container_layout.addWidget(
            self.next_page_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # previous reports container

        self.previous_reports_container_widget = QWidget(self)
        self.previous_reports_container_widget.setObjectName(
            "PreviousReportsContainerWidget"
        )
        self.previous_reports_container_widget.setVisible(False)
        self.main_layout.addWidget(self.previous_reports_container_widget, 1)

        self.previous_reports_container_layout = QVBoxLayout(
            self.previous_reports_container_widget
        )
        self.previous_reports_container_layout.setContentsMargins(0, 0, 0, 0)
        self.previous_reports_container_layout.setSpacing(20)
        self.previous_reports_container_widget.setLayout(
            self.previous_reports_container_layout
        )

        self.previous_reports_label = QLabel("Reporte Anteriores", self)
        self.previous_reports_label.setObjectName("PreviousReportsLabel")
        self.previous_reports_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.previous_reports_container_layout.addWidget(self.previous_reports_label)

        self.previous_reports_list_widget = ListWidget(self)
        self.previous_reports_container_layout.addWidget(
            self.previous_reports_list_widget
        )

    def change_operation_mode(self, mode: str):
        """
        Change the operation mode between Single End and Paired End.
        :param mode: The operation mode to set ('SingleEnd' or 'PairedEnd').
        """
        if mode.replace(" ", "") == "SingleEnd":
            self.select_input_2_widget.setVisible(False)
        elif mode.replace(" ", "") == "PairedEnd":
            self.select_input_2_widget.setVisible(True)

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
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
