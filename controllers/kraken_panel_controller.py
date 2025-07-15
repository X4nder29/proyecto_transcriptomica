import os
from typing import Callable, Optional, Tuple
from pathlib import Path
from PySide6.QtCore import QProcess
from views.main_window.panels import KrakenPanel
from views.main_window.panels.kraken_panel.widgets import (
    PreviousReportItemWidget,
)
from views.widgets import SelectFilePushButton, SavedConfigItemWidget
from utils import (
    win_to_wsl,
    clear_layout,
    get_krakened_files_paths,
    get_kraken2_output_folder_path,
    get_kraken2_database_folders,
    get_kraken2_saved_configs,
    set_kraken2_saved_config,
    get_kraken2_saved_config,
    remove_kraken2_saved_config,
    get_source_files_paths,
    get_trimmed_files_paths,
)


class KrakenPanelController:
    selected_input_file_1: Optional[Path] = None
    selected_input_file_2: Optional[Path] = None
    selected_database: Optional[Path] = None

    def __init__(self, view: KrakenPanel):
        self.view = view

        self._load_existing_report()

        self.kraken_procces = QProcess()
        self.kraken_procces.readyReadStandardOutput.connect(self._on_kraken_stdout)
        self.kraken_procces.readyReadStandardError.connect(self._on_kraken_stderr)
        self.kraken_procces.finished.connect(self._on_kraken_finished)

        self.krona_procces = QProcess()
        self.krona_procces.readyReadStandardOutput.connect(self._on_krona_stdout)
        self.krona_procces.readyReadStandardError.connect(self._on_krona_stderr)
        self.krona_procces.finished.connect(self._on_krona_finished)

        self.view.head.database_download_manager_button.clicked.connect(
            self._open_database_manager
        )
        self.view.head.cli_push_button.clicked.connect(self._show_command)
        self.view.head.star_button.clicked.connect(self._open_save_config_dialog)

        self.view.body.currentChanged.connect(self._change_page)

        # upload files page

        self.view.body.files_page.select_file_1.clicked.connect(
            lambda: self._open_file_selector_dialog(
                button=self.view.body.files_page.select_file_1,
                on_file=lambda file: setattr(self, "selected_input_file_1", file),
            )
        )
        self.view.body.files_page.select_file_2.clicked.connect(
            lambda: self._open_file_selector_dialog(
                button=self.view.body.files_page.select_file_2,
                on_file=lambda file: setattr(self, "selected_input_file_1", file),
            )
        )
        self.view.body.files_page.select_database_button.clicked.connect(
            self._open_database_selector_dialog
        )

        # options page

        self.view.body.files_page.next_page_button.clicked.connect(
            self._to_options_page
        )
        self.view.body.options_page.back_button.clicked.connect(self._go_back)
        self.view.body.options_page.taxonomize_button.clicked.connect(
            self._checking_existing_report
        )

        # generation page

        self.view.body.generation_page_widget.cancel_button.clicked.connect(
            self._cancel_kraken_command
        )

    # database manager

    def _open_database_manager(self):
        """
        Open the Kraken2 database manager.
        """
        from views.widgets import DatabaseManagerDialog
        from controllers import KrakenDatabaseManagerController

        database_manager_dialog = DatabaseManagerDialog(parent=self.view)
        KrakenDatabaseManagerController(database_manager_dialog)
        database_manager_dialog.show()

    # checking

    def _load_existing_report(self):
        files = get_krakened_files_paths()

        if not files:
            self.view.body.files_page.previous_reports_container_widget.setVisible(
                False
            )
            print(f"{Path(__file__).name}", "-", "No Krakened files found.")
            return

        self.view.body.files_page.previous_reports_container_widget.setVisible(True)

        for i in range(
            self.view.body.files_page.previous_reports_list_widget.scroll_content_layout.count()
        ):
            item = self.view.body.files_page.previous_reports_list_widget.scroll_content_layout.itemAt(
                i
            )

            if item.widget():
                item.widget().deleteLater()

        for file in files:
            file_list_item = PreviousReportItemWidget(
                file.name,
                str(file),
                parent=self.view.body.files_page.previous_reports_list_widget,
            )
            file_list_item.open_action.clicked.connect(
                lambda _, f=file: os.startfile(f.parent.as_posix())
            )
            file_list_item.delete_action.clicked.connect(
                lambda _, f=file: self._show_delete_source_file_dialog(f)
            )
            file_list_item.clicked.connect(
                lambda f=file: self._open_webview(f.as_posix())
            )
            self.view.body.files_page.previous_reports_list_widget.scroll_content_layout.addWidget(
                file_list_item
            )

    def _checking_existing_report(self):
        mode = (
            self.view.body.files_page.operation_mode_widget.button_group.checkedButton().text()
        )

        if mode == "Single End":
            krona_html = (
                get_kraken2_output_folder_path()
                / f"{self.selected_input_file_1.stem}_report.krona.html"
            )
            kraken_txt = (
                get_kraken2_output_folder_path()
                / f"{self.selected_input_file_1.stem}_report.txt"
            )

        if mode == "Paired End":
            krona_html = (
                get_kraken2_output_folder_path()
                / f"{self.selected_input_file_1.stem}_{self.selected_input_file_2.stem}.krona.html"
            )
            kraken_txt = (
                get_kraken2_output_folder_path()
                / f"{self.selected_input_file_1.stem}_{self.selected_input_file_2.stem}_report.txt"
            )

        print(f"{Path(__file__).name}", "-", "Krona HTML report path:", krona_html)
        print(f"{Path(__file__).name}", "-", "Kraken TXT report path:", kraken_txt)

        if krona_html.exists() and kraken_txt.exists():

            print(f"{Path(__file__).name}", "-", "Krona report and Kraken report found.")
            self._reset_upload_files_values()
            self._reset_options_values()
            self._go_back()
            self._open_webview(krona_html.as_posix())
            return

        print(f"{Path(__file__).name}", "-", "No existing report found.")
        self._run_kraken_command()

    def _show_delete_source_file_dialog(self, source_file: Path):
        """
        Show a confirmation dialog before deleting a source file.
        """
        from PySide6.QtWidgets import QMessageBox

        reply = QMessageBox.question(
            self.view,
            "Delete Source File",
            f"Are you sure you want to delete {source_file.name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self._delete_file(source_file)

    def _delete_file(self, file: Path):
        """
        Delete the source file from the workspace.
        """
        if not file.exists():
            return

        try:
            if file.exists():
                file.unlink(missing_ok=True)  # Remove the file if it exists

            self._load_existing_report()
        except Exception as e:
            print(f"Error deleting file {file}: {e}")

    def _checking_existing_databases(self) -> bool:
        """
        Returns True if there is at least one existing directory in `db_paths`
        that contains one or more `.k2d` files; otherwise shows a warning and
        returns False.
        """
        databases = get_kraken2_database_folders()

        has_k2d = any(path.exists() and any(path.glob("*.k2d")) for path in databases)

        if not databases or not has_k2d:
            from PySide6.QtWidgets import QMessageBox

            # Creamos el QMessageBox manualmente para poder añadir botones
            msg = QMessageBox(self.view)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("No downloaded databases found.")

            # Botón por defecto para cerrar
            close_btn = msg.addButton(QMessageBox.Close)
            # Botón personalizado para lanzar el gestor de bases
            download_btn = msg.addButton("Download Database...", QMessageBox.AcceptRole)

            msg.exec()  # Espera a que el usuario pulse algo

            clicked = msg.clickedButton()
            if clicked == download_btn:
                self._open_database_manager()

            return False

        return True

    # kraken

    def _generate_kraken_command(self) -> Tuple[str, list[str]]:
        """
        Generate the command to run Kraken based on the selected options.
        """

        arguments = [
            "kraken2",
        ]

        # operation mode

        mode = (
            self.view.body.files_page.operation_mode_widget.button_group.checkedButton().text()
        )

        # input files check

        if mode == "Single End":
            required = [self.selected_input_file_1]
            msg = "Debe seleccionar un archivo de entrada."
        else:
            required = [self.selected_input_file_1, self.selected_input_file_2]
            msg = "Debe seleccionar dos archivos de entrada."

        if any(file is None for file in required):
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self.view,
                "Error",
                msg,
            )
            return "", []

        # database

        if self.selected_database is None:
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self.view,
                "Error",
                "Debe seleccionar una base de datos de Kraken2.",
            )

            return "", []

        arguments.extend(
            [
                "--db",
                f"{win_to_wsl(self.selected_database).as_posix()}",
            ]
        )

        # threads

        threads = self.view.body.options_page.threads_selector_widget.slider.value()
        if threads > 0:
            arguments.extend(["--threads", f"{threads}"])

        # report

        output_folder_path = get_kraken2_output_folder_path()

        if output_folder_path is None:
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self.view,
                "Error",
                "La carpeta de salida de los reportes de Kraken2 no está configurada o no existe.",
            )
            return "", []

        if mode == "Single End":
            report_output_path = (
                output_folder_path / f"{self.selected_input_file_1.stem}_report.txt"
            )
        else:
            report_output_path = (
                output_folder_path
                / f"{self.selected_input_file_1.stem}_{self.selected_input_file_2.stem}_report.txt"
            )

        arguments.extend(
            [
                "--report",
                f"{win_to_wsl(report_output_path).as_posix()}",
            ]
        )

        # output

        arguments.extend(
            [
                "--output",
                "-",
            ]
        )  # Output to standard output (stdout)

        # quick

        is_quick_active = self.view.body.options_page.quick.checkbox.isChecked()
        if is_quick_active:
            arguments.append("--quick")

        # memory mapping

        is_memory_mapping_active = (
            self.view.body.options_page.memory_mapping.checkbox.isChecked()
        )
        if is_memory_mapping_active:
            arguments.append("--memory-mapping")

        # confidence

        is_confidence_active = (
            self.view.body.options_page.confidence.checkbox.isChecked()
        )

        if is_confidence_active:
            confidence_value = self.view.body.options_page.confidence.decimal_selector_suboption_widget.decimal_selector._spin_box.value()
            if confidence_value >= 0.0 and confidence_value <= 1.0:
                arguments.extend(
                    [
                        "--confidence",
                        f"{confidence_value}",
                    ]
                )

        # minimum hit groups

        is_minimum_hit_groups_active = (
            self.view.body.options_page.minimum_hit_groups.checkbox.isChecked()
        )

        if is_minimum_hit_groups_active:
            minimum_hit_groups = (
                self.view.body.options_page.minimum_hit_groups.number_selector_suboption_widget.number_selector._spin_box.value()
            )
            if minimum_hit_groups > 0:
                arguments.extend(
                    [
                        "--minimum-hit-groups",
                        f"{minimum_hit_groups}",
                    ]
                )

        # minimum base quality

        is_minimum_base_quality_active = (
            self.view.body.options_page.minimum_base_quality.checkbox.isChecked()
        )
        if is_minimum_base_quality_active:
            minimum_base_quality = (
                self.view.body.options_page.minimum_base_quality.number_selector_suboption_widget.number_selector._spin_box.value()
            )
            if minimum_base_quality > 0:
                arguments.extend(
                    [
                        "--minimum-base-quality",
                        f"{minimum_base_quality}",
                    ]
                )

        # input files

        if mode == "Single End":
            arguments.append(f"{win_to_wsl(self.selected_input_file_1).as_posix()}")

        if mode == "Paired End":
            arguments.extend(
                [
                    "--paired",
                    f"{win_to_wsl(self.selected_input_file_1).as_posix()}",
                    f"{win_to_wsl(self.selected_input_file_2).as_posix()}",
                ]
            )

        # return command and arguments

        return "wsl", arguments

    def _show_command(self):
        """
        Show the generated command in the Kraken panel.
        """
        command, args = self._generate_kraken_command()

        from views.widgets import CliDialog

        cli_dialog = CliDialog(self.view)
        cli_dialog.set_command(command + " " + " ".join(args))
        cli_dialog.show()

    def _run_kraken_command(self):
        """
        Run the generated command in the Kraken panel.
        """
        """ if not self._checking_existing_databases():
            return """

        command, args = self._generate_kraken_command()

        if not command or not args:
            return

        # Create the command string
        self.view.body.setCurrentIndex(2)  # Navigate to the generation page
        self.kraken_procces.kill()  # Kill any previous process
        self.kraken_procces.setProgram(command)
        self.kraken_procces.setArguments(args)
        self.kraken_procces.setProcessChannelMode(
            QProcess.ProcessChannelMode.MergedChannels
        )
        self.kraken_procces.start()
        print(Path(__file__).name, "-", "Running command:", command, args)

    def _cancel_kraken_command(self):
        """
        Cancel the currently running command in the Kraken panel.
        """
        if self.kraken_procces.state() == QProcess.ProcessState.Running:
            self.kraken_procces.kill()  # Kill the running process
        self.view.body.setCurrentIndex(0)  # Navigate back to the upload page

    def _on_kraken_stdout(self):
        data = (
            self.kraken_procces.readAllStandardOutput().data().decode(errors="ignore")
        )
        print(
            Path(__file__).name, "-", "kraken2-info", "-", data
        )  # Print the standard output to the console
        if data.strip() == "Loading database information...":
            self.view.body.generation_page_widget.title_label.setText(
                "Cargando información de la base de datos..."
            )

    def _on_kraken_stderr(self):
        data = self.kraken_procces.readAllStandardError().data().decode(errors="ignore")
        print(Path(__file__).name, "-", "error", "-", data)

    def _on_kraken_finished(self, exit_code: int, _: QProcess.ExitStatus):
        """Handle the completion of the Kraken process."""
        if exit_code != 0:
            print(
                f"{Path(__file__).name}",
                "-",
                "Kraken command failed with exit code:",
                exit_code,
            )
            self._reset_options_values()
            self.view.body.setCurrentIndex(0)  # Navigate back to the upload page
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self.view,
                "Error",
                "El comando de Kraken2 falló. Por favor, revisa la salida del comando.",
            )
            return

        print(f"{Path(__file__).name}", "-", "Command finished.")
        self._run_krona_command()
        self.view.body.generation_page_widget.cancel_button.clicked.connect(
            self._cancel_krona_command
        )

    def _reset_options_values(self):
        self.view.body.options_page.threads_selector_widget.slider.setValue(1)

        self.view.body.options_page.quick.checkbox.setChecked(False)
        self.view.body.options_page.memory_mapping.checkbox.setChecked(False)

        self.view.body.options_page.minimum_hit_groups.checkbox.setChecked(False)
        self.view.body.options_page.minimum_hit_groups.set_value(0)

        self.view.body.options_page.minimum_base_quality.checkbox.setChecked(False)
        self.view.body.options_page.minimum_base_quality.set_value(0)

        self.view.body.options_page.confidence.checkbox.setChecked(False)
        self.view.body.options_page.confidence.set_value(0.0)

    def _reset_upload_files_values(self):
        """
        Reset the values of the upload files page.
        """
        self.selected_input_file_1 = None
        self.selected_input_file_2 = None
        self.selected_database = None

        self.view.body.files_page.select_file_1.clear_file()
        self.view.body.files_page.select_file_2.clear_file()
        self.view.body.files_page.select_database_button.clear_file()

        self.view.body.files_page.operation_mode_widget.button_group.buttons()[
            0
        ].setChecked(True)
        self.view.body.files_page.select_input_2_widget.setVisible(False)

    # krona

    def _generate_krona_command(self) -> Tuple[str, list[str]]:
        """
        Generate the command to run Krona based on the Kraken report.
        """

        arguments = [
            "ktImportText",
        ]

        mode = self.view.body.files_page.operation_mode_widget.button_group.checkedButton().text()

        if mode == "Single End":
            input_file = win_to_wsl(
                get_kraken2_output_folder_path()
                / f"{self.selected_input_file_1.stem}_report.txt"
            )
            output_file = input_file.with_suffix(".krona.html")

            arguments.extend(
                [
                    "-o",
                    output_file.as_posix(),
                    input_file.as_posix(),
                ]
            )

        if mode == "Paired End":
            input_file = win_to_wsl(
                get_kraken2_output_folder_path()
                / f"{self.selected_input_file_1.stem}_{self.selected_input_file_2.stem}_report.txt"
            )
            output_file = input_file.with_suffix(".krona.html")

            arguments.extend(
                [
                    "-o",
                    output_file.as_posix(),
                    input_file.as_posix(),
                ]
            )

        return "wsl", arguments

    def _run_krona_command(self):
        """
        Run the Krona command to visualize the Kraken report.
        """
        command, args = self._generate_krona_command()

        if not command or not args:
            print(Path(__file__).name, "-", "No command to run Krona.")
            return

        self.krona_procces.kill()  # Kill any previous process
        self.krona_procces.setProgram(command)
        self.krona_procces.setArguments(args)
        self.krona_procces.setProcessChannelMode(
            QProcess.ProcessChannelMode.MergedChannels
        )
        self.krona_procces.start()
        print(Path(__file__).name, "-", "Running Krona command:", command, args)

    def _cancel_krona_command(self):
        """
        Cancel the currently running Krona command.
        """
        if self.krona_procces.state() == QProcess.ProcessState.Running:
            self.krona_procces.kill()  # Kill the running Krona process
        self.view.body.setCurrentIndex(0)  # Navigate back to the upload page

    def _on_krona_stdout(self):
        data = self.krona_procces.readAllStandardOutput().data().decode(errors="ignore")
        print(data)

    def _on_krona_stderr(self):
        data = self.krona_procces.readAllStandardError().data().decode(errors="ignore")
        print(data)

    def _on_krona_finished(self):
        """Handle the completion of the Krona process."""

        mode = self.view.body.files_page.operation_mode_widget.button_group.checkedButton().text()

        if mode == "Single End":
            krona_html = (
                get_kraken2_output_folder_path()
                / f"{self.selected_input_file_1.stem}_report.krona.html"
            )

        if mode == "Paired End":
            krona_html = (
                get_kraken2_output_folder_path()
                / f"{self.selected_input_file_1.stem}_{self.selected_input_file_2.stem}_report.krona.html"
            )

        self._open_webview(krona_html.as_posix())
        print(f"{Path(__file__).name}", "-", "Krona command finished.")

        self._reset_upload_files_values()
        self._reset_options_values()
        self._load_existing_report()
        self.view.body.setCurrentIndex(0)

    def _open_webview(self, url: str):
        from PySide6.QtWidgets import QMainWindow
        from PySide6.QtWebEngineWidgets import QWebEngineView
        from PySide6.QtCore import QUrl

        # Crear nueva ventana secundaria con QWebEngineView
        self.web_window = QMainWindow()
        self.web_window.setWindowTitle("Visor Web")
        self.web_window.resize(800, 600)

        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl.fromLocalFile(url))

        self.web_window.setCentralWidget(self.web_view)
        self.web_window.show()

    # Navigation

    def _change_page(self, index: int):
        """Change the current page of the Kraken panel."""
        if index == 1:
            self.view.head.star_button.setVisible(True)
            self.view.head.cli_push_button.setVisible(True)
            self._load_saved_config()
        else:
            self.view.head.star_button.setVisible(False)
            self.view.head.cli_push_button.setVisible(False)

        mode = (
            self.view.body.files_page.operation_mode_widget.button_group.checkedButton().text()
        )

        if index == 1:
            if mode == "Single End":
                required = [self.selected_input_file_1]
            else:
                required = [self.selected_input_file_1, self.selected_input_file_2]

            print(
                f"{Path(__file__).name}",
                "-",
                "Selected input files:",
                all(file.suffix == ".fastq" for file in required),
            )

            if all(file is not None for file in required) and all(
                file.suffix == ".fastq" for file in required
            ):

                self.view.body.options_page.minimum_base_quality.setVisible(True)
        else:
            self.view.body.options_page.minimum_base_quality.setVisible(False)

    def _to_options_page(self):
        """Navigate to the options page in the Kraken panel."""
        mode = (
            self.view.body.files_page.operation_mode_widget.button_group.checkedButton().text()
        )

        if mode == "Single End":
            required = [self.selected_input_file_1]
            msg = "Debe seleccionar un archivo de entrada."
        else:
            required = [self.selected_input_file_1, self.selected_input_file_2]
            msg = "Debe seleccionar dos archivos de entrada."

        if any(file is None for file in required):
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self.view,
                "Error",
                msg,
            )
            return

        if self.selected_database is None:
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self.view,
                "Error",
                "Debe seleccionar una base de datos de Kraken2.",
            )
            return

        self.view.body.setCurrentIndex(1)

    def _go_back(self):
        """Go back to the previous page in the Kraken panel."""
        if self.view.body.currentIndex() == 2:
            self.view.body.setCurrentIndex(0)  # Navigate back to the CLI page
            print(f"{Path(__file__).name}", "-", "Going back to the upload page")
        elif self.view.body.currentIndex() == 1:
            self.view.body.setCurrentIndex(0)
            print(f"{Path(__file__).name}", "-", "Going back to the upload page")

        self._reset_options_values()

    # Select files

    def _open_file_selector_dialog(
        self,
        button: SelectFilePushButton,
        on_file: Callable[[Path], None],
        on_cancel: Optional[Callable[[], None]] = None,
    ):
        from views.widgets import FileSelectorDialog

        file_selector_dialog = FileSelectorDialog(
            icon=":/assets/file.svg",
            files=get_source_files_paths() + get_trimmed_files_paths(),
            parent=self.view,
            filters=True,
            multiple=False,
        )
        result = file_selector_dialog.exec_()

        if result == FileSelectorDialog.DialogCode.Accepted:
            selected_input_file = file_selector_dialog.checked_files[0]
            button.set_file(selected_input_file.name, selected_input_file.as_posix())
            on_file(selected_input_file)
            print(
                Path(__file__).name,
                "-",
                "Selected input file:",
                selected_input_file,
            )
        else:
            if on_cancel:
                on_cancel()
                button.clear_file()
            print(Path(__file__).name, "-", "FileSelectorDialog rejected")

    # Select database

    def _open_database_selector_dialog(self):

        databases = get_kraken2_database_folders()

        if not databases:
            self._open_database_manager()
            return

        from views.widgets import FileSelectorDialog

        """ from controllers import FileSelectorDialogController """

        file_selector_dialog = FileSelectorDialog(
            icon=":/assets/database.svg",
            files=databases,
            parent=self.view,
        )
        """ file_selector_dialog_controller = FileSelectorDialogController(
            file_selector_dialog
        ) """
        result = file_selector_dialog.exec_()

        if result == FileSelectorDialog.DialogCode.Accepted:
            self.selected_database = file_selector_dialog.checked_files[0]
            self.view.body.files_page.select_database_button.set_file(
                self.selected_database.name,
                self.selected_database.as_posix(),
            )
            print(
                f"{Path(__file__).name}",
                "-",
                "Selected database:",
                self.selected_database,
            )
        else:
            self.selected_database = None
            self.view.body.files_page.select_database_button.clear_file()
            print("FileSelectorDialog rejected")

    # Save config

    def _open_save_config_dialog(self):
        """
        Open a dialog to save the current configuration of the Kraken panel.
        This method can be used to save the selected input files, database, and options.
        """
        from views.widgets import SaveConfigDialog

        save_config_dialog = SaveConfigDialog(self.view)
        save_config_dialog.exec_()

        if save_config_dialog.result() == SaveConfigDialog.DialogCode.Accepted:
            self._save_config(save_config_dialog.config_name.text())
            print(f"{Path(__file__).name}", "-", "Configuration saved successfully.")
        else:
            print(f"{Path(__file__).name}", "-", "Configuration saving canceled.")

    def _load_saved_config(self):
        """
        Load the saved configuration of the Kraken panel.
        This method can be used to restore the selected input files, database, and options.
        """
        clear_layout(self.view.body.options_page.list_widget.scroll_content_layout)

        configs = get_kraken2_saved_configs()

        if not configs:
            self.view.body.options_page.saved_configurations_widget.setVisible(False)
            print(f"{Path(__file__).name}", "-", "No saved configurations found.")
            return

        self.view.body.options_page.saved_configurations_widget.setVisible(True)
        print(f"{Path(__file__).name}", "-", "Loading saved configurations...")

        for config in configs:
            config_item_widget = SavedConfigItemWidget(
                config,
                parent=self.view.body.options_page.list_widget.scroll_content_widget,
            )
            config_item_widget.load_action.clicked.connect(
                lambda _, c=config: self._load_config(c)
            )
            config_item_widget.delete_action.clicked.connect(
                lambda _, c=config: self._delete_config(c)
            )
            self.view.body.options_page.list_widget.scroll_content_layout.addWidget(
                config_item_widget
            )

    def _save_config(self, name: str):
        """
        Save the current configuration of the Kraken panel.
        This method can be used to save the selected input files, database, and options.
        """
        data = {
            "threads": self.view.body.options_page.threads_selector_widget.slider.value(),
            "quick": self.view.body.options_page.quick.is_checked(),
            "memory_mapping": self.view.body.options_page.memory_mapping.is_checked(),
            "confidence": {
                "active": self.view.body.options_page.confidence.is_checked(),
                "value": self.view.body.options_page.confidence.value(),
            },
            "minimum_hit_groups": {
                "active": self.view.body.options_page.minimum_hit_groups.is_checked(),
                "value": self.view.body.options_page.minimum_hit_groups.value(),
            },
            "minimum_base_quality": {
                "active": self.view.body.options_page.minimum_base_quality.is_checked(),
                "value": self.view.body.options_page.minimum_base_quality.value(),
            },
        }

        set_kraken2_saved_config(
            name,
            data,
        )

        self._load_saved_config()

    def _load_config(self, name: str):
        """
        Load the saved configuration of the Kraken panel.
        This method can be used to restore the selected input files, database, and options.
        """
        config = get_kraken2_saved_config(name)

        if config is None:
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self.view,
                "Error",
                f"No configuration found with the name '{name}'.",
            )
            return

        # Threads
        value: int = config.get("threads", None)
        if value is not None and isinstance(value, int):
            self.view.body.options_page.threads_selector_widget.slider.setValue(value)
        else:
            print(Path(__file__).name, "-", "No threads value found in config.")

        # Quick
        value: bool = config.get("quick", False)
        self.view.body.options_page.quick.set_checked(value)

        # Memory mapping
        value: bool = config.get("memory_mapping", False)
        self.view.body.options_page.memory_mapping.set_checked(value)

        # Confidence
        value_dict: dict = config.get("confidence", None)
        if value is not None and isinstance(value_dict, dict):
            value: bool = value_dict.get("active", False)
            self.view.body.options_page.confidence.set_checked(value)

            value: float = value_dict.get("value", None)
            if value is not None and isinstance(value, float):
                self.view.body.options_page.confidence.set_value(value)
            else:
                print(Path(__file__).name, "-", "No confidence value found in config.")
        else:
            print(Path(__file__).name, "-", "No confidence value found in config.")

        # Minimum hit groups
        value_dict: dict = config.get("minimum_hit_groups", None)
        if value_dict is not None and isinstance(value_dict, dict):
            value: bool = value_dict.get("active", False)
            self.view.body.options_page.minimum_hit_groups.set_checked(value)

            value: int = value_dict.get("value", None)
            if value is not None and isinstance(value, int):
                self.view.body.options_page.minimum_hit_groups.set_value(value)
            else:
                print(
                    Path(__file__).name,
                    "-",
                    "No minimum hit groups value found in config.",
                )
        else:
            print(
                Path(__file__).name, "-", "No minimum hit groups value found in config."
            )

        # Minimum base quality
        value_dict: dict = config.get("minimum_base_quality", None)
        if value_dict is not None and isinstance(value_dict, dict):
            value: bool = value_dict.get("active", False)
            self.view.body.options_page.minimum_base_quality.set_checked(value)

            value: int = value_dict.get("value", None)
            if value is not None and isinstance(value, int):
                self.view.body.options_page.minimum_base_quality.set_value(config["minimum_base_quality"]["value"])
            else:
                print(
                    Path(__file__).name,
                    "-",
                    "No minimum base quality value found in config.",
                )
        else:
            print(
                Path(__file__).name,
                "-",
                "No minimum base quality value found in config.",
            )

        print(f"{Path(__file__).name}", "-", f"Configuration '{name}' loaded.")

    def _delete_config(self, name: str):
        """
        Delete the saved configuration of the Kraken panel.
        This method can be used to clear any saved settings or preferences.
        """
        from PySide6.QtWidgets import QMessageBox

        reply = QMessageBox.question(
            self.view,
            "Delete Configuration",
            f"Are you sure you want to delete the configuration '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            remove_kraken2_saved_config(name)
            self._load_saved_config()
            print(f"{Path(__file__).name}", "-", f"Configuration '{name}' deleted.")
