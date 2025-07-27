from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QScrollArea,
    QStyleOption,
    QStyle,
    QPushButton
)
from PySide6.QtGui import QPainter, QIcon
from PySide6.QtCore import Qt, QFile, QTextStream
from .widgets import (
    SettingsArea,
    SimpleActionItem,
    InstalledProgramItem,
    InstalledDependencyItem,
)


class SettingsPanelBody(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.load_stylesheet()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("SettingsPanelBody")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

        scrollarea = QScrollArea(self)
        scrollarea.setWidgetResizable(True)
        scrollarea.setObjectName("ScrollArea")
        scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.main_layout.addWidget(scrollarea)

        self.scroll_content = QWidget(scrollarea)
        self.scroll_content.setObjectName("ScrollContent")
        scrollarea.setWidget(self.scroll_content)

        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(20)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.scroll_content.setLayout(self.scroll_layout)

        # General Settings Section

        self.manual = SimpleActionItem(
            icon=QIcon(":/assets/user_manual.svg"),
            title="Manual de Usuario",
            action="Abrir",
            subtitle="Guía completa de uso del software",
            parent=self.scroll_content,
        )
        self.scroll_layout.addWidget(self.manual, 0, 0)

        # Installed Programs Section

        self.installed_programs_area = SettingsArea(
            self.scroll_content, "Programas instalados"
        )
        self.scroll_layout.addWidget(self.installed_programs_area)

        self.fastqc_program = InstalledProgramItem(
            icon=QIcon(":/assets/graphics.svg"),
            title="FastQC",
            subtitle="Herramienta de control de calidad"
        )
        self.installed_programs_area.add_item(self.fastqc_program)

        self.trimmomatic_program = InstalledProgramItem(
            icon=QIcon(":/assets/cut.svg"),
            title="Trimmomatic",
            subtitle="Herramienta de recorte de secuencias",
        )
        self.installed_programs_area.add_item(self.trimmomatic_program)

        self.sortmerna_program = InstalledProgramItem(
            icon=QIcon(":/assets/sort.svg"),
            title="SortMeRNA",
            subtitle="Herramienta de filtrado de ARN ribosómico",
        )
        self.installed_programs_area.add_item(self.sortmerna_program)

        self.kraken2_installed = InstalledProgramItem(
            icon=QIcon(":/assets/kraken.svg"),
            title="Kraken2",
            subtitle="Herramienta de clasificación taxonómica",
        )
        self.installed_programs_area.add_item(self.kraken2_installed)

        # Dependencies Section

        self.dependency_area = SettingsArea(self.scroll_content, "Dependencias")
        self.scroll_layout.addWidget(self.dependency_area)

        self.java_installed = InstalledDependencyItem(
            icon=QIcon(":/assets/java.svg"),
            title="Java",
            subtitle="Requerido para algunas herramientas",
        )
        self.dependency_area.add_item(self.java_installed)

        self.wsl_installed = InstalledDependencyItem(
            icon=QIcon(":/assets/wsl.svg"),
            title="WSL",
            subtitle="Windows Subsystem for Linux",
        )
        self.dependency_area.add_item(self.wsl_installed)

        self.krona_installed = InstalledDependencyItem(
            icon=QIcon(":/assets/krona.svg"),
            title="Krona",
            subtitle="Herramienta de visualización de datos taxonómicos",
        )
        self.dependency_area.add_item(self.krona_installed)

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
