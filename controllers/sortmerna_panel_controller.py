from os import startfile
from shutil import rmtree
from typing import Callable, Optional, Tuple
from pathlib import Path
from PySide6.QtCore import QProcess, Qt
from PySide6.QtGui import QFontMetrics
from views.main_window.panels.sortmerna_panel import SortMeRnaPanel
from views.main_window.panels.sortmerna_panel.widgets import PreviousReportItemWidget
from views.widgets import (
    FileSelectorDialog,
    SelectFilePushButton,
    SavedConfigItemWidget,
)
from utils import (
    OperationModes,
    clear_layout,
    get_sortmerna_executable_path,
    get_sortmerna_output_folder_path,
    get_source_files_paths,
    get_sorted_folders_paths,
    get_trimmed_files_paths,
    get_sortmerna_databases_files,
    get_sortmerna_databases,
    add_sortmerna_database,
    remove_sortmerna_database_by_link,
    get_sortmerna_databases_folder_from_settings,
    get_sortmerna_databases_folder_path,
    get_sortmerna_saved_configs,
    get_sortmerna_saved_config,
    set_sortmerna_saved_config,
    remove_sortmerna_saved_config
)


class SortMeRnaPanelController:

    selected_input_file_1: Optional[Path] = None
    selected_input_file_2: Optional[Path] = None
    selected_reference: Optional[Path] = None

    def __init__(self, view: SortMeRnaPanel):

        self.view = view

        self._load_existing_report()

        # process

        self.process = QProcess()
        self.process.setProcessChannelMode(
            QProcess.ProcessChannelMode.ForwardedOutputChannel
        )
        self.process.readyReadStandardOutput.connect(self._on_stdout)
        self.process.readyReadStandardError.connect(self._on_stderr)
        self.process.finished.connect(self._on_finished)
        self.view.body.generation_page.cancel_button.clicked.connect(
            self._cancel_command
        )

        # head
        self.view.head.cli_push_button.clicked.connect(self._show_command)
        self.view.head.database_download_manager_button.clicked.connect(
            self._open_database_manager
        )
        self.view.head.star_button.clicked.connect(self._open_save_config_dialog)
        self.view.head.user_manual_button.clicked.connect(self.open_user_manual)

        # select files

        self.view.body.files_page.select_file_1.clicked.connect(
            lambda: self._open_file_selector_dialog(
                self.view.body.files_page.select_file_1,
                lambda file: setattr(self, "selected_input_file_1", file),
                lambda: setattr(self, "selected_input_file_1", None),
            )
        )
        self.view.body.files_page.select_file_2.clicked.connect(
            lambda: self._open_file_selector_dialog(
                self.view.body.files_page.select_file_2,
                lambda file: setattr(self, "selected_input_file_2", file),
                lambda: setattr(self, "selected_input_file_2", None),
            )
        )

        # select references
        self.view.body.files_page.select_database_button.clicked.connect(
            self._open_references_selector_dialog
        )

        # navigation
        self.view.body.currentChanged.connect(self.change_page)
        self.view.body.files_page.next_page_button.clicked.connect(
            self._go_to_options_page
        )
        self.view.body.options_page.back_button.clicked.connect(self._go_back)

        # run command
        self.view.body.options_page.filter_button.clicked.connect(self._run_command)

    #

    def _load_existing_report(self):
        folders = get_sorted_folders_paths()

        if not folders:
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

        for file in folders:
            file_list_item = PreviousReportItemWidget(
                file.name,
                str(file),
                parent=self.view.body.files_page.previous_reports_list_widget,
            )
            file_list_item.open_action.clicked.connect(
                lambda _, f=file: startfile(f.as_posix())
            )
            file_list_item.delete_action.clicked.connect(
                lambda _, f=file: self._show_delete_source_file_dialog(f)
            )
            self.view.body.files_page.previous_reports_list_widget.scroll_content_layout.addWidget(
                file_list_item
            )

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
                rmtree(file)

            self._load_existing_report()
        except Exception as e:
            print(f"Error deleting file {file}: {e}")

    # cli push button

    def _show_command(self):
        command, arguments = self._generate_command()
        print(f"Generated command: {command}")

        if command is None:
            return

        from views.widgets import CliDialog

        cli_dialog = CliDialog(self.view)
        cli_dialog.set_command(command.as_posix() + " " + " ".join(arguments))
        cli_dialog.show()

    # database manager

    def _open_database_manager(self):
        """
        Open the Kraken2 database manager.
        """
        from views.widgets import DatabaseManagerDialog
        from controllers import DatabaseManagerController

        db_folder = get_sortmerna_databases_folder_from_settings()

        database_manager_dialog = DatabaseManagerDialog(parent=self.view)
        DatabaseManagerController(
            database_manager_dialog,
            get_sortmerna_databases,
            get_sortmerna_databases_files,
            db_folder if db_folder else get_sortmerna_databases_folder_path(),
            add_sortmerna_database,
            remove_sortmerna_database_by_link,
        )
        database_manager_dialog.show()

    # command

    def _generate_command(self) -> Optional[Tuple[Path, list[str]]]:
        """Generate the command to run SortMeRna."""

        arguments = []

        mode = (
            self.view.body.files_page.operation_mode_widget.button_group.checkedButton().text()
        )

        if self.selected_input_file_1 is None:
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self.view,
                "Input File Missing",
                "Please select at least one input file.",
            )
            return None

        if (
            self.selected_input_file_2 is None
            and mode != OperationModes.SingleEnd.value[0]
        ):
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self.view,
                "Input File Missing",
                "Please select a second input file for paired-end mode.",
            )
            return None

        # references
        if self.selected_reference == []:
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self.view,
                "Reference File Missing",
                "Please select at least one reference file.",
            )
            return None

        if self.selected_reference is not None:
            arguments.extend(["--ref", f"{self.selected_reference.as_posix()}"])

        # input files
        files = (
            ["--reads", f"{self.selected_input_file_1}"]
            if mode == OperationModes.SingleEnd.value[0]
            else [
                "--reads",
                f"{self.selected_input_file_1}",
                "--reads",
                f"{self.selected_input_file_2}",
            ]
        )

        if files != []:
            arguments.extend(files)

        # threads
        threads = self.view.body.options_page.threads_selector_widget.slider.value()
        arguments.extend(["--threads", f"{threads}"])

        # use fastx
        arguments.append("--fastx")

        # unaligned
        is_unaligned_active = self.view.body.options_page.output_no_aligned.is_checked()
        if is_unaligned_active:
            arguments.append("--other")

        # output sam
        is_output_sam_active = (
            self.view.body.options_page.output_sam.checkbox.isChecked()
        )
        if is_output_sam_active:
            arguments.append("--sam")

        # include sq tags
        is_include_sq_tags_active = (
            self.view.body.options_page.include_sq_tags.checkbox.isChecked()
        )
        if is_include_sq_tags_active:
            arguments.append("--SQ")

        # blast format
        is_blast_format_active = (
            self.view.body.options_page.blast_format.checkbox.isChecked()
        )
        if is_blast_format_active:
            blast_format = (
                self.view.body.options_page.blast_format.combo_box.currentData()
            )
            arguments.extend(["--blast", f"{blast_format}"])

        # num alignments
        is_num_alignments_active = (
            self.view.body.options_page.num_alignments.checkbox.isChecked()
        )
        if is_num_alignments_active:
            num_alignments = self.view.body.options_page.num_alignments.value()
            print(num_alignments)
            arguments.extend(["--num_alignments", f"{num_alignments}"])

        # min lis
        is_min_lis_active = self.view.body.options_page.min_lis.checkbox.isChecked()
        if is_min_lis_active:
            min_lis = self.view.body.options_page.min_lis.value()
            arguments.extend(["--min_lis", f"{min_lis}"])

        # no best
        is_no_best_active = self.view.body.options_page.no_best.checkbox.isChecked()
        if is_no_best_active:
            arguments.append("--no-best")

        # paired
        is_paired_active = self.view.body.options_page.paired.checkbox.isChecked()
        if is_paired_active:
            arguments.append("--paired")

        # workdir

        workdir = get_sortmerna_output_folder_path(self.selected_input_file_1.stem)

        if workdir is None:
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self.view,
                "Output Directory Error",
                "Could not create output directory for SortMeRna.",
            )
            return None

        arguments.extend(
            [
                "--workdir",
                workdir.as_posix(),
            ]
        )

        return get_sortmerna_executable_path(), arguments

    def _run_command(self):
        command, arguments = self._generate_command()

        print(f"Running command: {command}")

        if command is None:
            return

        self.view.body.setCurrentIndex(2)  # Navigate to the generation page

        self.process.kill()  # Kill any previous process if running
        self.process.setProgram(command.as_posix())
        self.process.setArguments(arguments)
        self.process.start()

    def _cancel_command(self):
        if self.process.state() == QProcess.Running:
            self.process.kill()
            print("Process cancelled.")
        else:
            print("No process is running to cancel.")

        self.view.body.setCurrentIndex(0)  # Go back to the files page

    def _on_stdout(self):
        output = self.process.readAllStandardOutput().data().decode(errors="ignore")
        """ print(f"STDOUT: {output}") """

        self.view.body.generation_page.title_label.setText(
            QFontMetrics(self.view.body.generation_page.title_label.font()).elidedText(
                output.strip(),
                Qt.TextElideMode.ElideRight,
                200,
            )
        )

    def _on_stderr(self):
        error_output = (
            self.process.readAllStandardError().data().decode(errors="ignore")
        )
        print(f"STDERR: {error_output}")

        from PySide6.QtWidgets import QMessageBox

        QMessageBox.warning(
            self.view,
            "Error",
            f"An error occurred while running SortMeRna:\n{error_output}",
        )
        # Here you can update the UI with the error output if needed

    def _on_finished(self):
        exit_code = self.process.exitCode()

        if exit_code == 0:
            print("Process finished successfully.")
        else:
            print(f"Process finished with error code: {exit_code}")

        self.view.body.setCurrentIndex(0)  # Go back to the files page

    def _reset_options_values(self):
        """Reset the options values to their default state."""
        self.view.body.options_page.threads_selector_widget.slider.setValue(1)
        self.view.body.options_page.output_no_aligned.set_checked(False)
        self.view.body.options_page.output_sam.checkbox.setChecked(False)
        self.view.body.options_page.include_sq_tags.checkbox.setChecked(False)
        self.view.body.options_page.blast_format.checkbox.setChecked(False)
        self.view.body.options_page.num_alignments.setEnabled(True)
        self.view.body.options_page.num_alignments.checkbox.setChecked(False)
        self.view.body.options_page.num_alignments.set_value(0)
        self.view.body.options_page.min_lis.setEnabled(True)
        self.view.body.options_page.min_lis.checkbox.setChecked(False)
        self.view.body.options_page.min_lis.set_value(0)
        self.view.body.options_page.no_best.checkbox.setChecked(False)
        self.view.body.options_page.paired.checkbox.setChecked(False)

    # navigation

    def change_page(self, index: int):
        if index == 1:
            self.view.head.cli_push_button.setVisible(True)
            self.view.head.star_button.setVisible(True)
            self._load_saved_config()
        elif index == 0:
            self.view.head.cli_push_button.setVisible(False)
            self.view.head.star_button.setVisible(False)
            self._reset_options_values()

        mode = (
            self.view.body.files_page.operation_mode_widget.button_group.checkedButton().text()
        )

        if mode == "Single End":
            self.view.body.options_page.paired.setEnabled(True)
        else:
            self.view.body.options_page.paired.setEnabled(False)

    def _go_to_options_page(self):
        """Go to the options page."""
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

        if not self.selected_reference:
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self.view,
                "Error",
                "Debe seleccionar una referencia de SortMeRNA.",
            )
            return

        self.view.body.setCurrentIndex(1)

    def _go_back(self):
        """Go back to the previous page."""
        self.view.body.setCurrentIndex(0)

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

    def _open_references_selector_dialog(self):
        """Open a dialog to select reference files."""

        references = get_sortmerna_databases_files()

        if not references:
            self._open_database_manager()
            return

        file_selector_dialog = FileSelectorDialog(
            icon=":/assets/database.svg",
            files=references,
            parent=self.view,
        )
        result = file_selector_dialog.exec_()

        if result == FileSelectorDialog.DialogCode.Accepted:
            self.selected_reference = file_selector_dialog.checked_files[0]
            self.view.body.files_page.select_database_button.set_file(
                self.selected_reference.name,
                self.selected_reference.as_posix(),
            )
            print(
                f"{Path(__file__).name}",
                "-",
                "Selected references:",
                self.selected_reference,
            )
        else:
            self.view.body.files_page.select_database_button.clear_file()
            self.selected_reference = []
            print("FileSelectorDialog rejected")

        file_selector_dialog.deleteLater()

    # Save config

    def _open_save_config_dialog(self) -> None:
        """
        Open a dialog to save the current configuration of the SortMeRNA panel.
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

    def _load_saved_config(self) -> None:
        """
        Load the saved configuration of the SortMeRNA panel.
        This method can be used to restore the selected input files, database, and options.
        """
        clear_layout(self.view.body.options_page.list_widget.scroll_content_layout)

        configs = get_sortmerna_saved_configs()

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

    def _save_config(self, name: str) -> None:
        """
        Save the current configuration of the Kraken panel.
        This method can be used to save the selected input files, database, and options.
        """
        data = {
            "threads": self.view.body.options_page.threads_selector_widget.slider.value(),
            "unaligned": self.view.body.options_page.output_no_aligned.is_checked(),
            "sam": self.view.body.options_page.output_sam.checkbox.isChecked(),
            "include_sq_tags": self.view.body.options_page.include_sq_tags.checkbox.isChecked(),
            "blast_format": {
                "active": self.view.body.options_page.blast_format.checkbox.isChecked(),
                "value": self.view.body.options_page.blast_format.combo_box.currentIndex(),
            },
            "num_alignments": {
                "active": self.view.body.options_page.num_alignments.checkbox.isChecked(),
                "value": self.view.body.options_page.num_alignments.value(),
            },
            "min_lis": {
                "active": self.view.body.options_page.min_lis.checkbox.isChecked(),
                "value": self.view.body.options_page.min_lis.value(),
            },
            "no_best": self.view.body.options_page.no_best.checkbox.isChecked(),
            "paired": self.view.body.options_page.paired.checkbox.isChecked(),
        }

        print(f"{Path(__file__).name}", "-", f"data to save: {data}")

        set_sortmerna_saved_config(
            name,
            data,
        )

        self._load_saved_config()

    def _load_config(self, name: str) -> None:
        """
        Load the saved configuration of the Kraken panel.
        This method can be used to restore the selected input files, database, and options.
        """
        config = get_sortmerna_saved_config(name)

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

        # Unaligned
        value: bool = config.get("unaligned", None)
        if value is not None and isinstance(value, bool):
            self.view.body.options_page.output_no_aligned.set_checked(value)
        else:
            print(Path(__file__).name, "-", "No unaligned value found in config.")

        # SAM
        value: bool = config.get("sam", None)
        if value is not None and isinstance(value, bool):
            self.view.body.options_page.output_sam.checkbox.setChecked(value)
        else:
            print(Path(__file__).name, "-", "No SAM value found in config.")

        # Include SQ tags
        value: bool = config.get("include_sq_tags", None)
        if value is not None and isinstance(value, bool):
            self.view.body.options_page.include_sq_tags.checkbox.setChecked(value)
        else:
            print(Path(__file__).name, "-", "No include SQ tags value found in config.")

        # Blast format
        blast_format = config.get("blast_format", None)
        if blast_format is not None and isinstance(blast_format, dict):
            active = blast_format.get("active", False)
            value = blast_format.get("value", "blastn")
            self.view.body.options_page.blast_format.checkbox.setChecked(active)
            self.view.body.options_page.blast_format.combo_box.setCurrentIndex(value)
        else:
            print(Path(__file__).name, "-", "No blast format found in config.")

        # Num alignments
        num_alignments = config.get("num_alignments", None)
        if num_alignments is not None and isinstance(num_alignments, dict):
            active = num_alignments.get("active", False)
            value = num_alignments.get("value", 1)
            self.view.body.options_page.num_alignments.checkbox.setChecked(active)
            self.view.body.options_page.num_alignments.set_value(value)
        else:
            print(Path(__file__).name, "-", "No num alignments found in config.")

        # Min LIS
        min_lis = config.get("min_lis", None)
        if min_lis is not None and isinstance(min_lis, dict):
            active = min_lis.get("active", False)
            value = min_lis.get("value", 0)
            self.view.body.options_page.min_lis.checkbox.setChecked(active)
            self.view.body.options_page.min_lis.set_value(value)
        else:
            print(Path(__file__).name, "-", "No min LIS found in config.")

        # No best
        value: bool = config.get("no_best", None)
        if value is not None and isinstance(value, bool):
            self.view.body.options_page.no_best.checkbox.setChecked(value)
        else:
            print(Path(__file__).name, "-", "No no best value found in config.")

        # Paired
        value: bool = config.get("paired", None)
        if value is not None and isinstance(value, bool):
            self.view.body.options_page.paired.checkbox.setChecked(value)
        else:
            print(Path(__file__).name, "-", "No paired value found in config.")

    def _delete_config(self, name: str) -> None:
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
            remove_sortmerna_saved_config(name)
            self._load_saved_config()
            print(f"{Path(__file__).name}", "-", f"Configuration '{name}' deleted.")

    def open_user_manual(self):
        from views.support_window.support_window import SupportWindow
        from controllers.support_window_controller import SupportWindowController

        self.support_window = SupportWindow(self.view.window())
        self.support_window_controller = SupportWindowController(
            self.support_window, "SortMeRNA"
        )
        self.support_window.show()
