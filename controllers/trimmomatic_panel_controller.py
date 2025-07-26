import os
import json
from pathlib import Path
from typing import Callable, Optional, cast
from PySide6.QtCore import QProcess, QThreadPool
from utils import (
    get_current_workspace,
    get_source_files_paths,
    get_trimmed_files_paths,
    get_trimmomatic_adapters_path,
    get_trimmomatic_jar_path,
    get_trimmomatic_output_file_path,
    get_trimmomatic_output_1paired_file_path,
    get_trimmomatic_output_2paired_file_path,
    get_trimmomatic_output_1unpaired_file_path,
    get_trimmomatic_output_2unpaired_file_path,
    get_project_file_path,
    to_unc_path,
    clear_layout,
    OperationModes,
)
from views.main_window.panels.trimmomatic_panel import TrimmomaticPanel
from views.main_window.panels.trimmomatic_panel.widgets import PreviousReportItemWidget
from views.widgets import SaveConfigDialog, SavedConfigItemWidget, SelectFilePushButton
from workers import GenericWorker


class TrimmomaticPanelController:

    selected_input_file_1: Optional[Path] = None
    selected_input_file_2: Optional[Path] = None

    def __init__(self, view: TrimmomaticPanel):

        self.view = view

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.on_stdout)
        self.process.readyReadStandardError.connect(self.on_stderr)
        self.process.finished.connect(self.on_finished)

        self._load_available_adapters()

        self.view.head.user_manual_button.clicked.connect(self.open_user_manual)
        self.view.head.cli_push_button.clicked.connect(self._open_cli_dialog)
        self.view.head.star_button.clicked.connect(self.open_save_config_dialog)

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

        # options page

        self.view.body.options_page.trimmer_button.clicked.connect(self.run_proccess)

        # navigation

        self.view.body.currentChanged.connect(self._change_page)
        self.view.body.files_page.next_page_button.clicked.connect(
            self._to_options_page
        )
        self.view.body.options_page.back_button.clicked.connect(self._go_back)

    # previous trimms

    def _load_existing_report(self):
        self.view.body.files_page.previous_reports_container_widget.setVisible(False)
        self.view.body.files_page.list_widget.setVisible(False)

        self.pool = QThreadPool.globalInstance()

        self.worker = GenericWorker(get_trimmed_files_paths)
        self.worker.signals.finished.connect(self._on_load_existing_report_finished)
        self.worker.signals.error.connect(self._on_load_existing_report_error)
        self.pool.start(self.worker)

    def _on_load_existing_report_finished(self, files: list[Path]):
        self.view.body.files_page.previous_reports_container_widget.setVisible(True)
        self.view.body.files_page.list_widget.setVisible(True)
        self.view.body.files_page.loading_widget.setVisible(False)

        clear_layout(self.view.body.files_page.list_widget.scroll_content_layout)

        for file in files:
            file_list_item = PreviousReportItemWidget(
                file.name,
                str(file),
                parent=self.view.body.files_page.list_widget,
            )
            file_list_item.open_action.clicked.connect(
                lambda _, f=file: os.startfile(f.parent.as_posix())
            )
            file_list_item.delete_action.clicked.connect(
                lambda _, f=file: self._show_delete_source_file_dialog(f)
            )
            self.view.body.files_page.list_widget.scroll_content_layout.addWidget(
                file_list_item
            )

        print(f"{Path(__file__).name}", "-", "Existing Trimmed files loaded.")

    def _on_load_existing_report_error(self, error: str):
        self.view.body.files_page.previous_reports_container_widget.setVisible(True)
        self.view.body.files_page.previous_reports_list_widget.setVisible(False)
        self.view.body.files_page.loading_widget.setCurrentIndex(1)  # Show error state
        print(f"{Path(__file__).name}", "-", "Error loading existing reports:", error)

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

    #

    def _change_operation_mode(self, mode: int):
        """Change the operation mode of the trimmomatic panel."""
        if mode == 1:
            self.view.body.paired_input_file_widget.setVisible(False)
            self.view.body.simple_input_file_widget.setVisible(True)

        if mode == 2:
            self.view.body.simple_input_file_widget.setVisible(False)
            self.view.body.paired_input_file_widget.setVisible(True)

        self.view.body.simple_input_file_widget.select_file_button.clear_file()
        self.view.body.paired_input_file_widget.select_file_push_button_1.clear_file()
        self.view.body.paired_input_file_widget.select_file_push_button_2.clear_file()
        self.selected_input_file_1 = None
        self.selected_input_file_2 = None

    def _open_files_window(
        self,
        button: SelectFilePushButton,
        on_file: Callable[[Path], None],
        on_cancel: Optional[Callable[[], None]] = None,
    ):
        """Open the FilesWindow."""
        from views.widgets import FileSelectorDialog

        file_selector_dialog = FileSelectorDialog(
            icon=":/assets/file.svg",
            files=get_source_files_paths() + get_trimmed_files_paths(),
            parent=self.view,
            filters=True,
            multiple=False,
        )
        result = file_selector_dialog.exec_()

        if result == FileSelectorDialog.Accepted:
            selected_input_file = file_selector_dialog.checked_files[0]

            button.set_file(selected_input_file.stem, str(selected_input_file))
            on_file(selected_input_file)

        else:
            if on_cancel:
                on_cancel()
                button.clear_file(None)
            print("FilesWindow rejected")

    def _open_cli_dialog(self):
        arguments = self.generate_arguments()

        if not arguments:
            print("No arguments to run the process")
            self.view.show_error_dialog("Please select at least one option")
            return

        command = "java " + " ".join(arguments)

        if command == "java ":
            return

        from views.widgets import CliDialog

        cli_dialog = CliDialog(self.view)
        cli_dialog.set_command(command)
        cli_dialog.show()

    def _show_help(self):
        from PySide6.QtCore import Qt
        from views.support_window import SupportWindow

        self._support_window = SupportWindow(self.view.window())
        self._support_window.setWindowFlag(Qt.WindowType.Window)
        self._support_window.show()
        print("SupportWindow opened")

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

    # command

    def generate_arguments(self) -> list[str]:
        trimmomatic_jar_path = get_trimmomatic_jar_path()

        if not trimmomatic_jar_path:
            self.view.show_error_dialog(
                "Trimmomatic not found. Please install Trimmomatic and try again."
            )
            return []

        mode = (
            self.view.body.files_page.operation_mode_widget.button_group.checkedButton().text()
        )
        threads = self.view.body.options_page.threads_selector_widget.slider.value()
        phred = (
            self.view.body.options_page.quality_scores_format_options_widget.button_group.checkedButton().text()
        )

        arguments = [
            "-jar",
            f"{trimmomatic_jar_path}",
            (
                OperationModes.SingleEnd.value[1]
                if mode == OperationModes.SingleEnd.value[0]
                else OperationModes.PairedEnd.value[1]
            ),
            "-threads",
            str(threads),
            f"-phred{phred[-2:]}",
        ]

        # files for SE or PE mode

        if self.selected_input_file_1 is None and self.selected_input_file_2 is None:
            self.view.show_error_dialog("Please select an input file")
            return []

        files = (
            [
                self.selected_input_file_1.as_posix(),
                get_trimmomatic_output_file_path(
                    self.selected_input_file_1.stem
                ).as_posix(),
            ]
            if mode == OperationModes.SingleEnd.value[0]
            else [
                self.selected_input_file_1.as_posix(),
                self.selected_input_file_2.as_posix(),
                get_trimmomatic_output_1paired_file_path().as_posix(),
                get_trimmomatic_output_2paired_file_path().as_posix(),
                get_trimmomatic_output_1unpaired_file_path().as_posix(),
                get_trimmomatic_output_2unpaired_file_path().as_posix(),
            ]
        )

        arguments.extend(files)

        # illumina clip option
        is_illumina_clip_active = (
            self.view.body.options_page.illumina_clip_option_widget.checkbox.isChecked()
        )
        if is_illumina_clip_active:

            adapter = (
                self.view.body.options_page.illumina_clip_option_widget.adaptar_suboption.combo_box.currentData()
            )
            seed_mismatches = (
                self.view.body.options_page.illumina_clip_option_widget.seed_mismatches_suboption.number_selector._spin_box.value()
            )
            palindrome_clip_threshold = (
                self.view.body.options_page.illumina_clip_option_widget.palindrome_clip_threshold_suboption.number_selector._spin_box.value()
            )
            simple_clip_threshold = (
                self.view.body.options_page.illumina_clip_option_widget.simple_clip_threshold_suboption.number_selector._spin_box.value()
            )

            illumina_clip_arguments = f"ILLUMINACLIP:{to_unc_path(adapter)}:{seed_mismatches}:{palindrome_clip_threshold}:{simple_clip_threshold}"

            is_min_adapter_length_active = (
                self.view.body.options_page.illumina_clip_option_widget.min_adapter_length_suboption.check_box_widget.isChecked()
            )
            if is_min_adapter_length_active:
                min_adapter_length = (
                    self.view.body.options_page.illumina_clip_option_widget.min_adapter_length_suboption.number_selector._spin_box.value()
                )
                illumina_clip_arguments += f":{min_adapter_length}"
            else:
                illumina_clip_arguments += ":0"

            keep_both_reads = (
                self.view.body.options_page.illumina_clip_option_widget.keep_both_reads_suboption.checkbox.isChecked()
            )
            if keep_both_reads:
                illumina_clip_arguments += ":True"

            arguments.append(illumina_clip_arguments)

        # sliding window option
        is_sliding_window_active = (
            self.view.body.options_page.sliding_window_option_widget.checkbox.isChecked()
        )
        if is_sliding_window_active:
            window_size = (
                self.view.body.options_page.sliding_window_option_widget.window_size_suboption.number_selector._spin_box.value()
            )
            quality_threshold = (
                self.view.body.options_page.sliding_window_option_widget.quality_threshold_suboption.number_selector._spin_box.value()
            )
            arguments.append(f"SLIDINGWINDOW:{window_size}:{quality_threshold}")

        # leading option

        is_leading_active = (
            self.view.body.options_page.leading_option_widget.checkbox.isChecked()
        )
        if is_leading_active:
            leading = (
                self.view.body.options_page.leading_option_widget.number_selector_suboption_widget.number_selector._spin_box.value()
            )
            arguments.append(f"LEADING:{leading}")

        # trailing option
        is_trailing_active = (
            self.view.body.options_page.trailing_option_widget.checkbox.isChecked()
        )
        if is_trailing_active:
            trailing = (
                self.view.body.options_page.trailing_option_widget.number_selector_suboption_widget.number_selector._spin_box.value()
            )
            arguments.append(f"TRAILING:{trailing}")

        # minlen option
        is_minlen_active = (
            self.view.body.options_page.minlen_option_widget.checkbox.isChecked()
        )
        if is_minlen_active:
            minlen = (
                self.view.body.options_page.minlen_option_widget.number_selector_suboption_widget.number_selector._spin_box.value()
            )
            arguments.append(f"MINLEN:{minlen}")

        # crop option
        is_crop_active = (
            self.view.body.options_page.crop_option_widget.checkbox.isChecked()
        )
        if is_crop_active:
            crop = (
                self.view.body.options_page.crop_option_widget.number_selector_suboption_widget.number_selector._spin_box.value()
            )
            arguments.append(f"CROP:{crop}")

        # headcrop option
        is_headcrop_active = (
            self.view.body.options_page.headcrop_option_widget.checkbox.isChecked()
        )
        if is_headcrop_active:
            headcrop = (
                self.view.body.options_page.headcrop_option_widget.number_selector_suboption_widget.number_selector._spin_box.value()
            )
            arguments.append(f"HEADCROP:{headcrop}")

        # return the command arguments
        if (
            not is_illumina_clip_active
            and not is_sliding_window_active
            and not is_leading_active
            and not is_trailing_active
            and not is_minlen_active
            and not is_crop_active
            and not is_headcrop_active
        ):
            return []

        return arguments

    def run_proccess(self):
        arguments = self.generate_arguments()

        if not arguments:
            return

        """ self.view.head.indeterminate_progress_bar_background.setVisible(True)
        self.view.head.cancel_button.setVisible(True)
        self.view.head.play_button.setVisible(False)
        self.view.body.setEnabled(False) """

        self.process.start(
            "java",
            arguments,
        )

        self.view.body.setCurrentIndex(2)

    def kill_process(self):
        self.view.body.setEnabled(True)
        self.view.head.indeterminate_progress_bar_background.setVisible(False)
        self.view.head.cancel_button.setVisible(False)
        self.view.head.play_button.setVisible(True)
        if self.process.state() == QProcess.Running:
            self.process.kill()

            print("Process cancelled")
        else:
            print("No process running to cancel")

    def on_stdout(self):
        output = self.process.readAllStandardOutput().data().decode()
        self.view.body.generation_page_widget.title_label.setText(output)
        print("output", output)

    def on_stderr(self):
        error = self.process.readAllStandardError().data().decode()
        self.view.body.generation_page_widget.set_text(error)
        print("error", self.process.readAllStandardError().data().decode())

    def on_finished(self, exit_code, exit_status):
        """
        This method is called when the process finishes.
        It updates the UI and shows a message to the user.
        """
        if exit_status == QProcess.ExitStatus.NormalExit and exit_code == 0:
            pass

        self._go_back()
        self._load_existing_report()

    # save configs

    def open_save_config_dialog(self):
        save_config_dialog = SaveConfigDialog(self.view)
        save_config_dialog.exec()

        if save_config_dialog.result() == SaveConfigDialog.Accepted:
            print("SaveConfigDialog accepted")
            self.save_config(save_config_dialog.config_name.text())
            self.load_saved_configs()

    def load_saved_configs(self):

        clear_layout(self.view.body.options_page.list_widget.scroll_content_layout)

        project_file_path = get_project_file_path()

        if not project_file_path:
            self.view.show_error_dialog(
                "No project file found. Please create a project first."
            )
            return

        try:
            with open(project_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                configs = data.get("trimmomatic_configs", {})

                if not configs:
                    self.view.body.options_page.saved_configurations_widget.setVisible(
                        False
                    )
                    print(
                        f"{Path(__file__).name}", "-", "No saved configurations found"
                    )
                    return

                self.view.body.options_page.saved_configurations_widget.setVisible(True)
                print(f"{Path(__file__).name}", "-", "Loading saved configurations...")

                for config_name, _ in configs.items():
                    config_item_widget = SavedConfigItemWidget(
                        config_name,
                        parent=self.view.body.options_page.list_widget,
                    )
                    config_item_widget.load_action.clicked.connect(
                        lambda _, c=config_name: self.load_config(c)
                    )
                    config_item_widget.delete_action.clicked.connect(
                        lambda _, c=config_name: self.delete_config(c)
                    )
                    self.view.body.options_page.list_widget.scroll_content_layout.addWidget(
                        config_item_widget
                    )

                print(f"{Path(__file__).name}", "-", "Saved configurations loaded")

        except FileNotFoundError:
            self.view.show_error_dialog(
                "Project file not found. Please create a project first."
            )
            return

    def save_config(self, name):
        adapters_folder_path = get_trimmomatic_adapters_path()

        current_workspace_path = get_current_workspace()

        if not current_workspace_path:
            self.view.show_error_dialog(
                "No workspace found. Please create a workspace first."
            )
            return

        config_data = {
            "threads": self.view.body.options_page.threads_selector_widget.slider.value(),
            "phred": self.view.body.options_page.quality_scores_format_options_widget.button_group.checkedId(),
            "illumina_clip": {
                "active": self.view.body.options_page.illumina_clip_option_widget.checkbox.isChecked(),
                "adapter": cast(
                    Path,
                    self.view.body.options_page.illumina_clip_option_widget.adaptar_suboption.combo_box.currentData(),
                )
                .relative_to(adapters_folder_path)
                .name,
                "seed_mismatches": self.view.body.options_page.illumina_clip_option_widget.seed_mismatches_suboption.number_selector._spin_box.value(),
                "palindrome_clip_threshold": self.view.body.options_page.illumina_clip_option_widget.palindrome_clip_threshold_suboption.number_selector._spin_box.value(),
                "simple_clip_threshold": self.view.body.options_page.illumina_clip_option_widget.simple_clip_threshold_suboption.number_selector._spin_box.value(),
                "min_adapter_length_active": self.view.body.options_page.illumina_clip_option_widget.min_adapter_length_suboption.check_box_widget.isChecked(),
                "min_adapter_length": self.view.body.options_page.illumina_clip_option_widget.min_adapter_length_suboption.number_selector._spin_box.value(),
                "keep_both_reads": self.view.body.options_page.illumina_clip_option_widget.checkbox.isChecked(),
            },
            "leading": {
                "active": self.view.body.options_page.leading_option_widget.checkbox.isChecked(),
                "value": self.view.body.options_page.leading_option_widget.number_selector_suboption_widget.number_selector._spin_box.value(),
            },
            "trailing": {
                "active": self.view.body.options_page.trailing_option_widget.checkbox.isChecked(),
                "value": self.view.body.options_page.trailing_option_widget.number_selector_suboption_widget.number_selector._spin_box.value(),
            },
            "sliding_window": {
                "active": self.view.body.options_page.sliding_window_option_widget.checkbox.isChecked(),
                "window_size": self.view.body.options_page.sliding_window_option_widget.window_size_suboption.number_selector._spin_box.value(),
                "quality_threshold": self.view.body.options_page.sliding_window_option_widget.quality_threshold_suboption.number_selector._spin_box.value(),
            },
            "minlen": {
                "active": self.view.body.options_page.minlen_option_widget.checkbox.isChecked(),
                "value": self.view.body.options_page.minlen_option_widget.number_selector_suboption_widget.number_selector._spin_box.value(),
            },
            "crop": {
                "active": self.view.body.options_page.crop_option_widget.checkbox.isChecked(),
                "value": self.view.body.options_page.crop_option_widget.number_selector_suboption_widget.number_selector._spin_box.value(),
            },
            "headcrop": {
                "active": self.view.body.options_page.headcrop_option_widget.checkbox.isChecked(),
                "value": self.view.body.options_page.headcrop_option_widget.number_selector_suboption_widget.number_selector._spin_box.value(),
            },
        }

        project_file_path = get_project_file_path()

        if not project_file_path:
            self.view.show_error_dialog(
                "No project file found. Please create a project first."
            )
            return

        # Save the config data to the project file
        try:
            with open(project_file_path, "r+", encoding="utf-8") as f:
                data = json.load(f)
                data.setdefault("trimmomatic_configs", {})
                # Modificas datos existentes o añades
                data["trimmomatic_configs"][name.strip()] = config_data

                f.seek(0)  # Vuelve al comienzo del archivo
                json.dump(data, f, indent=4)
                f.truncate()  # Elimina todo lo que quede tras la actualización
        except FileNotFoundError:
            # Si no existe, crear y abrir en modo escritura
            initial = {"trimmomatic_configs": {name: config_data}}
            with open(project_file_path, "w", encoding="utf-8") as f:
                json.dump(initial, f, indent=4)

    def load_config(self, name):
        adapters_folder_path = get_trimmomatic_adapters_path()

        current_workspace_path = get_current_workspace()

        if not current_workspace_path:
            self.view.show_error_dialog(
                "No workspace found. Please create a workspace first."
            )
            return

        project_file_path = get_project_file_path()

        if not project_file_path:
            self.view.show_error_dialog(
                "No project file found. Please create a project first."
            )
            return

        # Save the config data to the project file
        try:
            with open(project_file_path, "r+", encoding="utf-8") as f:
                data = json.load(f)
                configs = data.get("trimmomatic_configs", {})
                config_data = configs.get(name)
                if not config_data:
                    self.view.show_error_dialog("Config not found")
                    return

                """ # Input files
                if config_data["selected_input_file_1"]:
                    self.selected_input_file_1 = (
                        current_workspace_path
                        / Path(config_data["selected_input_file_1"])
                    ).resolve()

                    self.view.body.simple_input_file_widget.select_file_button.set_file(
                        self.selected_input_file_1.stem,
                        self.selected_input_file_1.as_posix(),
                    )

                if config_data["selected_input_file_2"]:
                    self.selected_input_file_2 = (
                        current_workspace_path
                        / Path(config_data["selected_input_file_2"])
                    ).resolve()

                    self.view.body.paired_input_file_widget.select_file_push_button_2.set_file(
                        self.selected_input_file_2.stem,
                        self.selected_input_file_2.as_posix(),
                    ) """

                """ # Operation mode
                self.view.body.fil.ooperation_mode_widget.button_group.button(
                    1 if config_data["mode"] == OperationModes.SingleEnd.value[0] else 2
                ).setChecked(True) """

                # Threads
                self.view.body.options_page.threads_selector_widget.slider.setValue(
                    config_data["threads"]
                )

                # Phred
                self.view.body.options_page.quality_scores_format_options_widget.button_group.button(
                    config_data["phred"]
                ).setChecked(
                    True
                )

                self.view.body.options_page.illumina_clip_option_widget.checkbox.setChecked(
                    config_data["illumina_clip"]["active"]
                )
                self.view.body.options_page.illumina_clip_option_widget.adaptar_suboption.combo_box.setCurrentIndex(
                    self.view.body.options_page.illumina_clip_option_widget.adaptar_suboption.combo_box.findText(
                        config_data["illumina_clip"]["adapter"]
                    )
                )
                self.view.body.options_page.illumina_clip_option_widget.seed_mismatches_suboption.number_selector._spin_box.setValue(
                    config_data["illumina_clip"]["seed_mismatches"]
                )
                self.view.body.options_page.illumina_clip_option_widget.palindrome_clip_threshold_suboption.number_selector._spin_box.setValue(
                    config_data["illumina_clip"]["palindrome_clip_threshold"]
                )
                self.view.body.options_page.illumina_clip_option_widget.simple_clip_threshold_suboption.number_selector._spin_box.setValue(
                    config_data["illumina_clip"]["simple_clip_threshold"]
                )
                self.view.body.options_page.illumina_clip_option_widget.min_adapter_length_suboption.check_box_widget.setChecked(
                    config_data["illumina_clip"]["min_adapter_length_active"]
                )
                self.view.body.options_page.illumina_clip_option_widget.min_adapter_length_suboption.number_selector._spin_box.setValue(
                    config_data["illumina_clip"]["min_adapter_length"]
                )
                self.view.body.options_page.illumina_clip_option_widget.keep_both_reads_suboption.checkbox.setChecked(
                    config_data["illumina_clip"]["keep_both_reads"]
                )

                self.view.body.options_page.sliding_window_option_widget.checkbox.setChecked(
                    config_data["sliding_window"]["active"]
                )
                self.view.body.options_page.sliding_window_option_widget.window_size_suboption.number_selector._spin_box.setValue(
                    config_data["sliding_window"]["window_size"]
                )
                self.view.body.options_page.sliding_window_option_widget.quality_threshold_suboption.number_selector._spin_box.setValue(
                    config_data["sliding_window"]["quality_threshold"]
                )

                self.view.body.options_page.leading_option_widget.checkbox.setChecked(
                    config_data["leading"]["active"]
                )
                self.view.body.options_page.leading_option_widget.number_selector_suboption_widget.number_selector._spin_box.setValue(
                    config_data["leading"]["value"]
                )

                self.view.body.options_page.trailing_option_widget.checkbox.setChecked(
                    config_data["trailing"]["active"]
                )
                self.view.body.options_page.trailing_option_widget.number_selector_suboption_widget.number_selector._spin_box.setValue(
                    config_data["trailing"]["value"]
                )

                self.view.body.options_page.minlen_option_widget.checkbox.setChecked(
                    config_data["minlen"]["active"]
                )
                self.view.body.options_page.minlen_option_widget.number_selector_suboption_widget.number_selector._spin_box.setValue(
                    config_data["minlen"]["value"]
                )

                self.view.body.options_page.crop_option_widget.checkbox.setChecked(
                    config_data["crop"]["active"]
                )
                self.view.body.options_page.crop_option_widget.number_selector_suboption_widget.number_selector._spin_box.setValue(
                    config_data["crop"]["value"]
                )

                self.view.body.options_page.headcrop_option_widget.checkbox.setChecked(
                    config_data["headcrop"]["active"]
                )
                self.view.body.options_page.headcrop_option_widget.number_selector_suboption_widget.number_selector._spin_box.setValue(
                    config_data["headcrop"]["value"]
                )

        except FileNotFoundError:
            with open(project_file_path, "w", encoding="utf-8") as f:
                json.dump("{}", f, indent=4)

    def delete_config(self, name):
        from PySide6.QtWidgets import QMessageBox

        reply = QMessageBox.question(
            self.view,
            "Delete Configuration",
            f"Are you sure you want to delete the configuration '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            project_file_path = get_project_file_path()

            if not project_file_path:
                self.view.show_error_dialog(
                    "No project file found. Please create a project first."
                )
                return

            try:
                with open(project_file_path, "r+", encoding="utf-8") as f:
                    data = json.load(f)
                    configs = data.get("trimmomatic_configs", {})

                    if name in configs:
                        del configs[name]
                        data["trimmomatic_configs"] = configs

                        f.seek(0)
                        json.dump(data, f, indent=4)
                        f.truncate()

                        self.load_saved_configs()
                    else:
                        self.view.show_error_dialog("Config not found")

            except FileNotFoundError:
                self.view.show_error_dialog(
                    "Project file not found. Please create a project first."
                )

            self.load_saved_configs()
            print(f"{Path(__file__).name}", "-", f"Configuration '{name}' deleted.")

    def check_configs(self):
        pass

    # others

    def _load_available_adapters(self):
        """
        Load available adapters from the config file.
        """
        adapters_folder_path = get_trimmomatic_adapters_path()

        if adapters_folder_path is None:
            print(
                Path(__file__).name,
                "-",
                "Trimmomatic adapters folder not found. Please set the path in the config file.",
            )
            return

        adapters = [adapter.name for adapter in Path(adapters_folder_path).glob("*.fa")]
        self.view.body.options_page.illumina_clip_option_widget.adaptar_suboption.combo_box.clear()

        print(Path(__file__).name, "-", f"Available adapters: {adapters}")

        for adapter in adapters:
            self.view.body.options_page.illumina_clip_option_widget.adaptar_suboption.combo_box.addItem(
                adapter, userData=adapters_folder_path / adapter
            )

    def _reset_options_values(self):
        self.view.body.options_page.threads_selector_widget.slider.setValue(1)

        self.view.body.options_page.illumina_clip_option_widget.set_checked(False)
        self.view.body.options_page.illumina_clip_option_widget.adaptar_suboption.combo_box.setCurrentIndex(
            0
        )
        self.view.body.options_page.illumina_clip_option_widget.seed_mismatches_suboption.set_value(
            0
        )
        self.view.body.options_page.illumina_clip_option_widget.palindrome_clip_threshold_suboption.set_value(
            30
        )
        self.view.body.options_page.illumina_clip_option_widget.simple_clip_threshold_suboption.set_value(
            0
        )
        self.view.body.options_page.illumina_clip_option_widget.min_adapter_length_suboption.set_checked(
            False
        )
        self.view.body.options_page.illumina_clip_option_widget.min_adapter_length_suboption.set_value(
            0
        )
        self.view.body.options_page.illumina_clip_option_widget.keep_both_reads_suboption.set_checked(
            False
        )

        self.view.body.options_page.sliding_window_option_widget.set_checked(False)
        self.view.body.options_page.sliding_window_option_widget.window_size_suboption.set_value(
            0
        )
        self.view.body.options_page.sliding_window_option_widget.quality_threshold_suboption.set_value(
            0
        )

        self.view.body.options_page.quality_scores_format_options_widget.button_group.buttons()[
            0
        ].setChecked(
            True
        )  # Set Phred33 as default

        self.view.body.options_page.leading_option_widget.set_checked(False)
        self.view.body.options_page.leading_option_widget.number_selector_suboption_widget.set_value(
            0
        )

        self.view.body.options_page.trailing_option_widget.set_checked(False)
        self.view.body.options_page.trailing_option_widget.number_selector_suboption_widget.set_value(
            0
        )

        self.view.body.options_page.minlen_option_widget.set_checked(False)
        self.view.body.options_page.minlen_option_widget.number_selector_suboption_widget.set_value(
            0
        )

        self.view.body.options_page.crop_option_widget.set_checked(False)
        self.view.body.options_page.crop_option_widget.number_selector_suboption_widget.set_value(
            0
        )

        self.view.body.options_page.headcrop_option_widget.set_checked(False)
        self.view.body.options_page.headcrop_option_widget.number_selector_suboption_widget.set_value(
            0
        )

    def _reset_upload_files_values(self):
        """
        Reset the values of the upload files page.
        """
        self.selected_input_file_1 = None
        self.selected_input_file_2 = None
        self.selected_database = None

        self.view.body.files_page.select_file_1.clear_file()
        self.view.body.files_page.select_file_2.clear_file()

        self.view.body.files_page.operation_mode_widget.button_group.buttons()[
            0
        ].setChecked(True)
        self.view.body.files_page.select_input_2_widget.setVisible(False)

    # Navigation

    def _change_page(self, index: int):
        """Change the current page of the Kraken panel."""
        if index == 1:
            self.view.head.star_button.setVisible(True)
            self.view.head.cli_push_button.setVisible(True)
            self.load_saved_configs()
        else:
            self.view.head.star_button.setVisible(False)
            self.view.head.cli_push_button.setVisible(False)

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

    # open user manual

    def open_user_manual(self):
        from views.support_window.support_window import SupportWindow
        from controllers.support_window_controller import SupportWindowController

        self.support_window = SupportWindow(self.view.window())
        self.support_window_controller = SupportWindowController(self.support_window, "Trimmomatic")
        self.support_window.show()
