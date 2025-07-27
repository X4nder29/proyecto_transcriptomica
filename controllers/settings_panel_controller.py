from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QProcess
from views.main_window import SettingsPanel
from utils import (
    get_fastqc_file_path,
    get_fastqc_executable_path_from_settings,
    get_trimmomatic_jar_path,
    get_trimmomatic_executable_path_from_settings,
    get_sortmerna_executable_path,
    get_sortmerna_executable_path_from_settings,
)


class SettingsPanelController:

    wsl_process = QProcess()
    java_process = QProcess()
    kraken2_process = QProcess()
    krona_process = QProcess()

    is_wsl_installed = False
    is_java_installed = False
    is_fastqc_installed = False
    is_trimmomatic_installed = False
    is_sortmerna_installed = False
    is_kraken2_installed = False
    is_krona_installed = False

    def __init__(self, view: SettingsPanel):
        self.view = view

        self.view.content.manual.open_manual_push_button.clicked.connect(
            self._open_user_manual
        )

        self.view.content.wsl_installed.install_push_button.clicked.connect(
            self._open_user_manual_on_wsl
        )
        self.view.content.kraken2_installed.install_push_button.clicked.connect(
            self._open_user_manual_on_wsl
        )
        self.view.content.krona_installed.install_push_button.clicked.connect(
            self._open_user_manual_on_wsl
        )

        self.application = QApplication.instance()

        self.application.state.wsl_check_worker.result.connect(self._on_wsl_finished)
        self.application.state.java_check_worker.result.connect(
            self._on_java_check_finished
        )
        self.application.state.kraken2_check_worker.result.connect(
            self._on_kraken2_check_finished
        )
        self.application.state.krona_check_worker.result.connect(
            self._on_krona_check_finished
        )

    def check_installed(self):
        """
        Check if the required programs are installed on the system.
        This method is called when the settings panel
        is opened to update the installed status of WSL and Java.
        """
        self._check_installed_java()
        self._check_installed_wsl()
        self._check_installed_fastqc()
        self._check_installed_trimmomatic()
        self._check_installed_sortmerna()

    # WSL

    def _check_installed_wsl(self):
        print(Path(__file__).name, "-", "Checking WSL installation...")
        self.application.state.wsl_check_worker.start()

    def _on_wsl_finished(self, installed: bool):
        self.view.content.wsl_installed.set_installed(installed)
        print(Path(__file__).name, "-", "WSL installation status:", installed)

        if installed:
            self._check_installed_kraken2()
            self._check_installed_krona()

    # Java

    def _check_installed_java(self):
        print(Path(__file__).name, "-", "Checking Java installation...")
        self.application.state.java_check_worker.start()

    def _on_java_check_finished(self, installed: bool):
        self.view.content.java_installed.set_installed(installed)
        print(Path(__file__).name, "-", "Java installation status:", installed)

    # kraken2

    def _check_installed_kraken2(self):
        print(Path(__file__).name, "-", "Checking Kraken2 installation...")
        self.application.state.kraken2_check_worker.start()

    def _on_kraken2_check_finished(self, installed: bool):
        self.view.content.kraken2_installed.set_installed(installed)
        print(Path(__file__).name, "-", "Kraken2 installation status:", installed)

    # krona

    def _check_installed_krona(self):
        print(Path(__file__).name, "-", "Checking Krona installation...")
        self.application.state.krona_check_worker.start()

    def _on_krona_check_finished(self, installed: bool):
        self.view.content.krona_installed.set_installed(installed)
        print(Path(__file__).name, "-", "Krona installation status:", installed)

    # fastqc

    def _check_installed_fastqc(self):
        """
        Check if FastQC is installed on the system.
        """
        fastqc_executable = get_fastqc_executable_path_from_settings()
        if fastqc_executable is not None and fastqc_executable.exists():
            self.view.content.fastqc_program.set_installed(True)
            self.view.content.fastqc_program.set_path(fastqc_executable.as_posix())
            print(Path(__file__).name, "-", "FastQC is installed.")
            return

        fastqc_executable = get_fastqc_file_path()
        if fastqc_executable is not None and fastqc_executable.exists():
            self.view.content.fastqc_program.set_installed(True)
            self.view.content.fastqc_program.set_path(fastqc_executable.as_posix())
            print(Path(__file__).name, "-", "FastQC is installed.")
            return

        self.view.content.fastqc_program.set_installed(False)
        self.view.content.fastqc_program.clear_path()
        print(Path(__file__).name, "-", "FastQC is not installed.")

    # trimmomatic

    def _check_installed_trimmomatic(self):
        """
        Check if Trimmomatic is installed on the system.
        """
        trimmomatic_executable = get_trimmomatic_executable_path_from_settings()
        if trimmomatic_executable is not None and trimmomatic_executable.exists():
            self.view.content.trimmomatic_program.set_installed(True)
            self.view.content.trimmomatic_program.set_path(
                trimmomatic_executable.as_posix()
            )
            print(Path(__file__).name, "-", "Trimmomatic is installed.")
            return

        trimmomatic_jar = get_trimmomatic_jar_path()
        if trimmomatic_jar is not None and trimmomatic_jar.exists():
            self.view.content.trimmomatic_program.set_installed(True)
            self.view.content.trimmomatic_program.set_path(trimmomatic_jar.as_posix())
            print(Path(__file__).name, "-", "Trimmomatic is installed.")
            return

        self.view.content.trimmomatic_program.set_installed(False)
        self.view.content.trimmomatic_program.clear_path()
        print(Path(__file__).name, "-", "Trimmomatic is not installed.")

    # sortmerna

    def _check_installed_sortmerna(self):
        """
        Check if SortMeRNA is installed on the system.
        """
        sortmerna_executable = get_sortmerna_executable_path_from_settings()
        if sortmerna_executable is not None and sortmerna_executable.exists():
            self.view.content.sortmerna_program.set_installed(True)
            self.view.content.sortmerna_program.set_path(
                sortmerna_executable.as_posix()
            )
            print(Path(__file__).name, "-", "SortMeRNA is installed.")
            return

        sortmerna_executable = get_sortmerna_executable_path()
        if sortmerna_executable is not None and sortmerna_executable.exists():
            self.view.content.sortmerna_program.set_installed(True)
            self.view.content.sortmerna_program.set_path(
                sortmerna_executable.as_posix()
            )
            print(Path(__file__).name, "-", "SortMeRNA is installed.")
            return

        self.view.content.sortmerna_program.set_installed(False)
        self.view.content.sortmerna_program.clear_path()
        print(Path(__file__).name, "-", "SortMeRNA is not installed.")

    # Open manual

    def _open_user_manual(self):
        """ " """

        from controllers import SupportWindowController
        from views.support_window import SupportWindow

        self.support_window = SupportWindow()
        self.suuport_window_controller = SupportWindowController(self.support_window)
        self.support_window.show()

    def _open_user_manual_on_wsl(self):
        """
        Open the user manual in WSL.
        """

        from controllers import SupportWindowController
        from views.support_window import SupportWindow

        self.support_window = SupportWindow(self.view.window())
        self.suuport_window_controller = SupportWindowController(
            self.support_window, "WSL"
        )
        self.support_window.show()
