from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QStackedLayout,
    QMessageBox
)
from PySide6.QtCore import QFile, QTextStream


class HomeWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("TranscriptoHub")
        self.setWindowIcon(QIcon(":/assets/icon.svg"))
        self.setAcceptDrops(True)
        self.setWindowIcon(QIcon("assets/icon.svg"))

        self.settings = QSettings("preferences.ini", QSettings.IniFormat)
        print(self.settings.fileName())

        self.setupUi()

    def setupUi(self):

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.main_layout = QStackedLayout(central_widget)

        empty_file_panel = EmptyFilePanel(
            add_file_path=self.addFilePath
        )
        self.main_layout.addWidget(empty_file_panel)

        files_panel = FilesPanel(
            settings=self.settings,
            add_file_path=self.addFilePath,
            file_widget_click=self.checkFilesPaths,
        )
        self.main_layout.addWidget(files_panel)

        self.checkFilesPaths()

    def load_stylesheet(self):
        qss_file = QFile(f":/styles/{Path(__file__).stem}.qss")
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            qss_file.close()
