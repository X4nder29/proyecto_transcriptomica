from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QPushButton,
    QStyleOption,
    QStyle,
    QLabel,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from controllers.check_installed_programs import CheckInstalledPrograms


class ProgramsArea(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("ProgramsArea")
        self.setMinimumWidth(225)

        """ self.check_installed_programs = CheckInstalledPrograms()
        self.check_installed_programs.check_programs()
        self.check_installed_programs.java_finished.connect(lambda x: print(x))
        self.check_installed_programs.trimmomatic_finished.connect(lambda x: print(x)) """

        self.load_stylesheet()

        self.setup_ui()

    def setup_ui(self):

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        self.area_title = QLabel("Programs", self)
        self.area_title.setObjectName("AreaTitle")
        self.main_layout.addWidget(self.area_title)

        self.install_icon_outlined = QIcon("assets/install_outlined.svg")
        self.install_icon_filled = QIcon("assets/install_filled.svg")

        # trimmomatic program

        self.trimmomatic_program = QWidget(self)
        self.trimmomatic_program.setObjectName("Program")

        self.trimmomatic_program_layout = QHBoxLayout(self.trimmomatic_program)
        self.trimmomatic_program_layout.setContentsMargins(10, 5, 10, 5)
        self.trimmomatic_program_layout.setSpacing(50)

        self.trimmomatic_program_label = QLabel("Trimmomatic", self.trimmomatic_program)
        self.trimmomatic_program_layout.addWidget(self.trimmomatic_program_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.trimmomatic_program_button = QPushButton(self.trimmomatic_program)
        self.trimmomatic_program_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.trimmomatic_program_button.setIcon(self.install_icon_outlined)
        self.trimmomatic_program_button.setIconSize(QSize(20, 20))
        self.trimmomatic_program_button.setObjectName("InstallButton")
        self.trimmomatic_program_layout.addWidget(self.trimmomatic_program_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.main_layout.addWidget(self.trimmomatic_program)

        # java program

        self.java_program = QWidget(self)
        self.java_program.setObjectName("Program")

        self.java_program_layout = QHBoxLayout(self.java_program)
        self.java_program_layout.setContentsMargins(10, 5, 10, 5)
        self.java_program_layout.setSpacing(50)

        self.java_program_label = QLabel("Java", self.java_program)
        self.java_program_layout.addWidget(self.java_program_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.java_program_button = QPushButton(self.java_program)
        self.java_program_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.java_program_button.setIcon(self.install_icon_filled)
        self.java_program_button.setIconSize(QSize(20, 20))
        self.java_program_button.setObjectName("InstallButton")
        self.java_program_layout.addWidget(self.java_program_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.main_layout.addWidget(self.java_program)

        # sort me rna program

        self.sortme_rna_program = QWidget(self)
        self.sortme_rna_program.setObjectName("Program")

        self.sortme_rna_program_layout = QHBoxLayout(self.sortme_rna_program)
        self.sortme_rna_program_layout.setContentsMargins(10, 5, 10, 5)
        self.sortme_rna_program_layout.setSpacing(50)

        self.sortme_rna_program_label = QLabel("SortMeRNA", self.sortme_rna_program)
        self.sortme_rna_program_layout.addWidget(self.sortme_rna_program_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.sortme_rna_program_button = QPushButton(self.sortme_rna_program)
        self.sortme_rna_program_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.sortme_rna_program_button.setIcon(self.install_icon_outlined)
        self.sortme_rna_program_button.setIconSize(QSize(20, 20))
        self.sortme_rna_program_button.setObjectName("InstallButton")
        self.sortme_rna_program_layout.addWidget(self.sortme_rna_program_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.main_layout.addWidget(self.sortme_rna_program)

        # fastqc program

        self.fastqc_program = QWidget(self)
        self.fastqc_program.setObjectName("Program")

        self.fastqc_program_layout = QHBoxLayout(self.fastqc_program)
        self.fastqc_program_layout.setContentsMargins(10, 5, 10, 5)
        self.fastqc_program_layout.setSpacing(50)

        self.fastqc_program_label = QLabel("FastQC", self.fastqc_program)
        self.fastqc_program_layout.addWidget(self.fastqc_program_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.fastqc_program_button = QPushButton(self.fastqc_program)
        self.fastqc_program_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.fastqc_program_button.setIcon(self.install_icon_outlined)
        self.fastqc_program_button.setIconSize(QSize(20, 20))
        self.fastqc_program_button.setObjectName("InstallButton")
        self.fastqc_program_layout.addWidget(self.fastqc_program_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.main_layout.addWidget(self.fastqc_program)

        # kraken2 program

        self.kraken2_program = QWidget(self)
        self.kraken2_program.setObjectName("Program")

        self.kraken2_program_layout = QHBoxLayout(self.kraken2_program)
        self.kraken2_program_layout.setContentsMargins(10, 5, 10, 5)
        self.kraken2_program_layout.setSpacing(50)

        self.kraken2_program_label = QLabel("Kraken2", self.kraken2_program)
        self.kraken2_program_layout.addWidget(self.kraken2_program_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.kraken2_program_button = QPushButton(self.kraken2_program)
        self.kraken2_program_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.kraken2_program_button.setIcon(self.install_icon_outlined)
        self.kraken2_program_button.setIconSize(QSize(20, 20))
        self.kraken2_program_button.setObjectName("InstallButton")
        self.kraken2_program_layout.addWidget(self.kraken2_program_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.main_layout.addWidget(self.kraken2_program)

        self.main_layout.addStretch()

    def load_stylesheet(self):
        styles_path = Path(__file__).parent / "programs_area.qss"
        if styles_path.exists():
            with open(styles_path, "r") as styles:
                self.setStyleSheet(styles.read())
