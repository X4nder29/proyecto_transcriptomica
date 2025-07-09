import os
import json
from pathlib import Path
from sqlite3 import adapters
from typing import Callable, Optional, cast
from PySide6.QtCore import QProcess
from utils import (
    get_app_data_path,
    get_current_workspace,
    get_trimmomatic_adapters_path,
    get_trimmomatic_jar_path,
    get_trimmomatic_output_file_path,
    get_trimmomatic_output_1paired_file_path,
    get_trimmomatic_output_2paired_file_path,
    get_trimmomatic_output_1unpaired_file_path,
    get_trimmomatic_output_2unpaired_file_path,
    get_project_file_path,
    to_unc_path,
    OperationModes,
)
from views.main_window.panels.trimmomatic_panel import TrimmomaticPanel
from views.widgets import SaveConfigDialog, SavedConfigItemWidget
from views.widgets import SelectFilePushButton


class TrimmomaticPanelController:

    selected_input_file_1: Optional[Path] = None
    selected_input_file_2: Optional[Path] = None

    def __init__(self, view: TrimmomaticPanel):
        self.view = view
        self.process = QProcess()

        self.view.body.threads_selector_widget.help.clicked.connect(self._show_help)
        self.view.head.star_button.clicked.connect(self.open_save_config_dialog)

        self.load_saved_configs()
        self._load_available_adapters()

        self.process.readyReadStandardOutput.connect(self.on_stdout)
        self.process.readyReadStandardError.connect(self.on_stderr)
        self.process.finished.connect(self.on_finished)

        # header buttons
        self.view.head.cancel_button.clicked.connect(self.kill_process)
        self.view.head.play_button.clicked.connect(self.run_proccess)
        self.view.head.star_button.clicked.connect(
            lambda: (
                print("Selected file 1:", self.selected_input_file_1),
                print("Selected file 2:", self.selected_input_file_2),
            )
        )
        self.view.head.cli_push_button.clicked.connect(self._open_cli_dialog)

        # suboptions buttons
        self.view.body.operation_mode_widget.button_group.idClicked.connect(
            lambda id: self._change_operation_mode(id)
        )
        self.view.body.simple_input_file_widget.select_file_button.clicked.connect(
            lambda: self._open_files_window(
                button=self.view.body.simple_input_file_widget.select_file_button,
                on_file=lambda file: setattr(self, "selected_input_file_1", file),
            )
        )
        self.view.body.paired_input_file_widget.select_file_push_button_1.clicked.connect(
            lambda: self._open_files_window(
                button=self.view.body.paired_input_file_widget.select_file_push_button_1,
                on_file=lambda file: setattr(self, "selected_input_file_1", file),
            )
        )
        self.view.body.paired_input_file_widget.select_file_push_button_2.clicked.connect(
            lambda: self._open_files_window(
                button=self.view.body.paired_input_file_widget.select_file_push_button_2,
                on_file=lambda file: setattr(self, "selected_input_file_2", file),
            )
        )

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
        from views import FilesWindow
        from controllers import FilesWindowController

        files_window = FilesWindow(parent=self.view)
        files_window_controller = FilesWindowController(files_window)
        result = files_window.exec_()

        if result == FilesWindow.Accepted:
            selected_input_file = files_window_controller.selected_input_file

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

    # command

    def generate_arguments(self) -> list[str]:
        trimmomatic_jar_path = get_trimmomatic_jar_path()

        if not trimmomatic_jar_path:
            self.view.show_error_dialog(
                "Trimmomatic not found. Please install Trimmomatic and try again."
            )
            return []

        mode = self.view.body.operation_mode_widget.button_group.checkedButton().text()
        threads = self.view.body.threads_selector_widget.slider.value()
        phred = (
            self.view.body.quality_scores_format_options_widget.button_group.checkedButton().text()
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
                get_trimmomatic_output_file_path(self.selected_input_file_1.stem).as_posix(),
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
            self.view.body.illumina_clip_option_widget.checkbox.isChecked()
        )
        if is_illumina_clip_active:

            adapter = (
                self.view.body.illumina_clip_option_widget.adaptar_suboption.combo_box.currentData()
            )
            seed_mismatches = (
                self.view.body.illumina_clip_option_widget.seed_mismatches_suboption.number_selector._number_label.text()
            )
            palindrome_clip_threshold = (
                self.view.body.illumina_clip_option_widget.palindrome_clip_threshold_suboption.number_selector._number_label.text()
            )
            simple_clip_threshold = (
                self.view.body.illumina_clip_option_widget.simple_clip_threshold_suboption.number_selector._number_label.text()
            )

            illumina_clip_arguments = f"ILLUMINACLIP:{to_unc_path(adapter)}:{seed_mismatches}:{palindrome_clip_threshold}:{simple_clip_threshold}"

            is_min_adapter_length_active = (
                self.view.body.illumina_clip_option_widget.min_adapter_length_suboption.check_box_widget.isChecked()
            )
            if is_min_adapter_length_active:
                min_adapter_length = (
                    self.view.body.illumina_clip_option_widget.min_adapter_length_suboption.number_selector._number_label.text()
                )
                illumina_clip_arguments += f":{min_adapter_length}"
            else:
                illumina_clip_arguments += ":0"

            keep_both_reads = (
                self.view.body.illumina_clip_option_widget.keep_both_reads_suboption.checkbox.isChecked()
            )
            if keep_both_reads:
                illumina_clip_arguments += ":True"

            arguments.append(illumina_clip_arguments)

        # sliding window option
        is_sliding_window_active = (
            self.view.body.sliding_window_option_widget.checkbox.isChecked()
        )
        if is_sliding_window_active:
            window_size = (
                self.view.body.sliding_window_option_widget.window_size_suboption.number_selector._number_label.text()
            )
            quality_threshold = (
                self.view.body.sliding_window_option_widget.quality_threshold_suboption.number_selector._number_label.text()
            )
            arguments.append(f"SLIDINGWINDOW:{window_size}:{quality_threshold}")

        # leading option

        is_leading_active = self.view.body.leading_option_widget.checkbox.isChecked()
        if is_leading_active:
            leading = (
                self.view.body.leading_option_widget.number_selector_suboption_widget.number_selector._number_label.text()
            )
            arguments.append(f"LEADING:{leading}")

        # trailing option
        is_trailing_active = self.view.body.trailing_option_widget.checkbox.isChecked()
        if is_trailing_active:
            trailing = (
                self.view.body.trailing_option_widget.number_selector_suboption_widget.number_selector._number_label.text()
            )
            arguments.append(f"TRAILING:{trailing}")

        # minlen option
        is_minlen_active = self.view.body.minlen_option_widget.checkbox.isChecked()
        if is_minlen_active:
            minlen = (
                self.view.body.minlen_option_widget.number_selector_suboption_widget.number_selector._number_label.text()
            )
            arguments.append(f"MINLEN:{minlen}")

        # crop option
        is_crop_active = self.view.body.crop_option_widget.checkbox.isChecked()
        if is_crop_active:
            crop = (
                self.view.body.crop_option_widget.number_selector_suboption_widget.number_selector._number_label.text()
            )
            arguments.append(f"CROP:{crop}")

        # headcrop option
        is_headcrop_active = self.view.body.headcrop_option_widget.checkbox.isChecked()
        if is_headcrop_active:
            headcrop = (
                self.view.body.headcrop_option_widget.number_selector_suboption_widget.number_selector._number_label.text()
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

        #
        mode = self.view.body.mode_area.button_group.checkedButton().text()
        threads = self.view.body.threads_option.slider.value()
        phred = self.view.body.quality_scores_format_option.button_group.checkedId()

        # check if mode is selected
        if mode not in ["SE", "PE"]:
            self.view.show_error_dialog("Please select a mode (SE or PE)")
            return

        if mode == "SE":

            # files for SE mode
            input_file_se = self.view.body.files_area_se.input_file_se.line_edit.text()

            if not input_file_se:
                self.view.show_error_dialog("Please select an input file")
                return

            output_file_se = (
                self.view.body.files_area_se.output_file_se.line_edit.text()
            )

            if not output_file_se:
                self.view.show_error_dialog("Please select an output file")
                return

        else:

            # files for PE mode
            input_file_pe1 = (
                self.view.body.files_area_pe.output_file_2_pe.line_edit.text()
            )

            if not input_file_pe1:
                self.view.show_error_dialog("Please select input file 1 for PE mode")
                return

            input_file_pe2 = (
                self.view.body.files_area_pe.input_file_2_pe.line_edit.text()
            )

            if not input_file_pe2:
                self.view.show_error_dialog("Please select input file 2 for PE mode")
                return

            output_file_paired1 = (
                self.view.body.files_area_pe.output_file_1_pe.line_edit.text()
            )

            if not output_file_paired1:
                self.view.show_error_dialog("Please select output file 1 for PE mode")
                return

            output_file_paired2 = (
                self.view.body.files_area_pe.output_file_1_pe.line_edit.text()
            )

            if not output_file_paired2:
                self.view.show_error_dialog("Please select output file 2 for PE mode")
                return

            output_file_unpaired1 = (
                self.view.body.files_area_pe.output_file_2_pe.line_edit.text()
            )

            if not output_file_unpaired1:
                self.view.show_error_dialog(
                    "Please select output file 1 for unpaired reads"
                )
                return

            output_file_unpaired2 = (
                self.view.body.files_area_pe.output_file_2_pe.line_edit.text()
            )

            if not output_file_unpaired2:
                self.view.show_error_dialog(
                    "Please select output file 2 for unpaired reads"
                )
                return

        # trim steps

        # illumina clip
        is_illumina_clip_active = (
            self.view.body.illumina_clip_option.active_button.isChecked()
        )
        adapter = self.view.body.illumina_clip_option.adapter_options.currentData()
        seed_mismatches = (
            self.view.body.illumina_clip_option.seed_mismatches_input._number_label.text()
        )
        palindrome_clip_threshold = (
            self.view.body.illumina_clip_option.palindrome_clip_threshold_input._number_label.text()
        )
        simple_clip_threshold = (
            self.view.body.illumina_clip_option.simple_clip_threshold_input._number_label.text()
        )

        is_min_adapter_length_active = (
            self.view.body.illumina_clip_option.min_adapter_length_button.isChecked()
        )
        min_adapter_length = (
            self.view.body.illumina_clip_option.min_adapter_length_selector._number_label.text()
        )

        keep_both_reads = (
            self.view.body.illumina_clip_option.keep_both_reads_button.isChecked()
        )

        is_leading_active = self.view.body.leading_option.leading_button.isChecked()
        leading = self.view.body.leading_option.number_selector._number_label.text()

        is_trailing_active = self.view.body.trailing_option.leading_button.isChecked()
        trailing = self.view.body.trailing_option.number_selector._number_label.text()

        is_sliding_window_active = (
            self.view.body.slidingwindow_option.active_button.isChecked()
        )
        window_size = (
            self.view.body.slidingwindow_option.window_size_selector._number_label.text()
        )

        is_quality_threshold_active = (
            self.view.body.slidingwindow_option.active_button.isChecked()
        )
        quality_threshold = (
            self.view.body.slidingwindow_option.quality_threshold_selector._number_label.text()
        )

        is_minlen_active = self.view.body.minlen_option.leading_button.isChecked()
        minlen = self.view.body.minlen_option.number_selector._number_label.text()

        is_crop_active = self.view.body.crop_option.leading_button.isChecked()
        crop = self.view.body.crop_option.number_selector._number_label.text()

        if (
            not is_illumina_clip_active
            and not is_leading_active
            and not is_trailing_active
            and not is_sliding_window_active
            and not is_quality_threshold_active
            and not is_minlen_active
            and not is_crop_active
        ):
            self.view.show_error_dialog("Please select at least one trim step")
            return

        if threads < 1:
            self.view.show_error_dialog("Please select at least one thread")
            return

        if not input_file_se or not output_file_se:
            self.view.show_error_dialog("Please select input and output files")
            return

        if os.path.splitext(input_file_se)[1] != ".fastq":
            self.view.show_error_dialog("Input file must be a .fastq file")
            return

        if os.path.splitext(output_file_se)[1] != ".fastq":
            self.view.show_error_dialog("Output file must be a .fastq file")
            return

        trimmomatic_jar_path = get_trimmomatic_jar_path()
        print(f"Trimmomatic path: {trimmomatic_jar_path}")

        if not trimmomatic_jar_path:
            self.view.show_error_dialog(
                "Trimmomatic not found. Please install Trimmomatic and try again."
            )
            return

        arguments = [
            "-jar",
            f"{trimmomatic_jar_path}",
            mode,
            "-threads",
            str(threads),
            f"-phred{phred}",
        ]

        if mode == "PE":
            arguments.extend(
                [
                    f'"{input_file_pe1}"',
                    f'"{input_file_pe2}"',
                    f'"{output_file_paired1}"',
                    f'"{output_file_paired2}"',
                    f'"{output_file_unpaired1}"',
                    f'"{output_file_unpaired2}"',
                ]
            )
        else:
            arguments.extend(
                [
                    f'{input_file_se.replace("\\", "/")}',
                    # """ f'{output_file_se.replace("\\", "/")}', """
                    f'{settings.value("current_workspace", "")}/trimmed/trimmed.fastq',
                ]
            )

        if is_illumina_clip_active:
            illumina_clip_arguments = f"ILLUMINACLIP:{to_unc_path(adapter)}:{seed_mismatches}:{palindrome_clip_threshold}:{simple_clip_threshold}"
            if is_min_adapter_length_active:
                illumina_clip_arguments += f":{min_adapter_length}"
            if keep_both_reads:
                illumina_clip_arguments += ":True"
            arguments.append(illumina_clip_arguments)

        if is_leading_active:
            arguments.append(f"LEADING:{leading}")

        if is_trailing_active:
            arguments.append(f"TRAILING:{trailing}")

        if is_sliding_window_active:
            arguments.append(f"SLIDINGWINDOW:{window_size}:{quality_threshold}")

        if is_minlen_active:
            arguments.append(f"MINLEN:{minlen}")

        if is_crop_active:
            arguments.append(f"CROP:{crop}")

        return arguments

    def run_proccess(self):
        arguments = self.generate_arguments()

        if not arguments:
            return

        self.view.head.indeterminate_progress_bar_background.setVisible(True)
        self.view.head.cancel_button.setVisible(True)
        self.view.head.play_button.setVisible(False)
        self.view.body.setEnabled(False)

        self.process.start(
            "java",
            self.generate_arguments(),
        )

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
        print("output", self.process.readAllStandardOutput().data().decode())

    def on_stderr(self):
        print("error", self.process.readAllStandardError().data().decode())

    def on_finished(self, exit_code, exit_status):
        """
        This method is called when the process finishes.
        It updates the UI and shows a message to the user.
        """
        if exit_status == QProcess.ExitStatus.NormalExit and exit_code == 0:
            pass

        self.view.body.setEnabled(True)
        self.view.head.indeterminate_progress_bar_background.setVisible(False)
        self.view.head.cancel_button.setVisible(False)
        self.view.head.play_button.setVisible(True)

    # save configs

    def open_save_config_dialog(self):
        save_config_dialog = SaveConfigDialog(self.view)
        save_config_dialog.exec()

        if save_config_dialog.result() == SaveConfigDialog.Accepted:
            print("SaveConfigDialog accepted")
            self.save_config(save_config_dialog.config_name.text())
            self.load_saved_configs()

    def load_saved_configs(self):

        for index in range(self.view.body.config_list_widget.main_layout.count()):
            item = self.view.body.config_list_widget.list_layout.itemAt(index)

            if item is None:
                continue

            if item.widget():
                item.widget().deleteLater()

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

                for config_name, _ in configs.items():
                    config_item_widget = SavedConfigItemWidget(
                        config_name,
                        parent=self.view.body.config_list_widget.list_widget,
                    )
                    config_item_widget.load_action.clicked.connect(
                        lambda _, c=config_name: self.load_config(c)
                    )
                    config_item_widget.delete_action.clicked.connect(
                        lambda _, c=config_name: self.delete_config(c)
                    )
                    self.view.body.config_list_widget.list_layout.addWidget(
                        config_item_widget
                    )

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
            "selected_input_file_1": (
                self.selected_input_file_1.relative_to(
                    current_workspace_path
                ).as_posix()
                if self.selected_input_file_1
                else None
            ),
            "selected_input_file_2": (
                self.selected_input_file_2.relative_to(
                    current_workspace_path
                ).as_posix()
                if self.selected_input_file_2
                else None
            ),
            "mode": self.view.body.operation_mode_widget.button_group.checkedButton().text(),
            "threads": self.view.body.threads_selector_widget.slider.value(),
            "phred": self.view.body.quality_scores_format_options_widget.button_group.checkedId(),
            "illumina_clip": {
                "active": self.view.body.illumina_clip_option_widget.checkbox.isChecked(),
                "adapter": cast(
                    Path,
                    self.view.body.illumina_clip_option_widget.adaptar_suboption.combo_box.currentData(),
                )
                .relative_to(adapters_folder_path)
                .name,
                "seed_mismatches": self.view.body.illumina_clip_option_widget.seed_mismatches_suboption.number_selector._number_label.text(),
                "palindrome_clip_threshold": self.view.body.illumina_clip_option_widget.palindrome_clip_threshold_suboption.number_selector._number_label.text(),
                "simple_clip_threshold": self.view.body.illumina_clip_option_widget.simple_clip_threshold_suboption.number_selector._number_label.text(),
                "min_adapter_length_active": self.view.body.illumina_clip_option_widget.min_adapter_length_suboption.check_box_widget.isChecked(),
                "min_adapter_length": self.view.body.illumina_clip_option_widget.min_adapter_length_suboption.number_selector._number_label.text(),
                "keep_both_reads": self.view.body.illumina_clip_option_widget.checkbox.isChecked(),
            },
            "leading": {
                "active": self.view.body.leading_option_widget.checkbox.isChecked(),
                "value": self.view.body.leading_option_widget.number_selector_suboption_widget.number_selector._number_label.text(),
            },
            "trailing": {
                "active": self.view.body.trailing_option_widget.checkbox.isChecked(),
                "value": self.view.body.trailing_option_widget.number_selector_suboption_widget.number_selector._number_label.text(),
            },
            "sliding_window": {
                "active": self.view.body.sliding_window_option_widget.checkbox.isChecked(),
                "window_size": self.view.body.sliding_window_option_widget.window_size_suboption.number_selector._number_label.text(),
                "quality_threshold": self.view.body.sliding_window_option_widget.quality_threshold_suboption.number_selector._number_label.text(),
            },
            "minlen": {
                "active": self.view.body.minlen_option_widget.checkbox.isChecked(),
                "value": self.view.body.minlen_option_widget.number_selector_suboption_widget.number_selector._number_label.text(),
            },
            "crop": {
                "active": self.view.body.crop_option_widget.checkbox.isChecked(),
                "value": self.view.body.crop_option_widget.number_selector_suboption_widget.number_selector._number_label.text(),
            },
            "headcrop": {
                "active": self.view.body.headcrop_option_widget.checkbox.isChecked(),
                "value": self.view.body.headcrop_option_widget.number_selector_suboption_widget.number_selector._number_label.text(),
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

                # Input files
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
                    )

                # Operation mode
                self.view.body.operation_mode_widget.button_group.button(
                    1 if config_data["mode"] == OperationModes.SingleEnd.value[0] else 2
                ).setChecked(True)

                # Threads
                self.view.body.threads_selector_widget.slider.setValue(
                    config_data["threads"]
                )

                # Phred
                self.view.body.quality_scores_format_options_widget.button_group.button(
                    1 if config_data["phred"] == "Phred33" else 2
                ).setChecked(True)

                self.view.body.illumina_clip_option_widget.checkbox.setChecked(
                    config_data["illumina_clip"]["active"]
                )
                self.view.body.illumina_clip_option_widget.adaptar_suboption.combo_box.setCurrentIndex(
                    self.view.body.illumina_clip_option_widget.adaptar_suboption.combo_box.findText(
                        config_data["illumina_clip"]["adapter"]
                    )
                )
                self.view.body.illumina_clip_option_widget.seed_mismatches_suboption.number_selector._number_label.setText(
                    config_data["illumina_clip"]["seed_mismatches"]
                )
                self.view.body.illumina_clip_option_widget.palindrome_clip_threshold_suboption.number_selector._number_label.setText(
                    config_data["illumina_clip"]["palindrome_clip_threshold"]
                )
                self.view.body.illumina_clip_option_widget.simple_clip_threshold_suboption.number_selector._number_label.setText(
                    config_data["illumina_clip"]["simple_clip_threshold"]
                )
                self.view.body.illumina_clip_option_widget.min_adapter_length_suboption.check_box_widget.setChecked(
                    config_data["illumina_clip"]["min_adapter_length_active"]
                )
                self.view.body.illumina_clip_option_widget.min_adapter_length_suboption.number_selector._number_label.setText(
                    config_data["illumina_clip"]["min_adapter_length"]
                )
                self.view.body.illumina_clip_option_widget.keep_both_reads_suboption.checkbox.setChecked(
                    config_data["illumina_clip"]["keep_both_reads"]
                )

                self.view.body.sliding_window_option_widget.checkbox.setChecked(
                    config_data["sliding_window"]["active"]
                )
                self.view.body.sliding_window_option_widget.window_size_suboption.number_selector._number_label.setText(
                    config_data["sliding_window"]["window_size"]
                )
                self.view.body.sliding_window_option_widget.quality_threshold_suboption.number_selector._number_label.setText(
                    config_data["sliding_window"]["quality_threshold"]
                )

                self.view.body.leading_option_widget.checkbox.setChecked(
                    config_data["leading"]["active"]
                )
                self.view.body.leading_option_widget.number_selector_suboption_widget.number_selector._number_label.setText(
                    config_data["leading"]["value"]
                )

                self.view.body.trailing_option_widget.checkbox.setChecked(
                    config_data["trailing"]["active"]
                )
                self.view.body.trailing_option_widget.number_selector_suboption_widget.number_selector._number_label.setText(
                    config_data["trailing"]["value"]
                )

                self.view.body.minlen_option_widget.checkbox.setChecked(
                    config_data["minlen"]["active"]
                )
                self.view.body.minlen_option_widget.number_selector_suboption_widget.number_selector._number_label.setText(
                    config_data["minlen"]["value"]
                )

                self.view.body.crop_option_widget.checkbox.setChecked(
                    config_data["crop"]["active"]
                )
                self.view.body.crop_option_widget.number_selector_suboption_widget.number_selector._number_label.setText(
                    config_data["crop"]["value"]
                )

                self.view.body.headcrop_option_widget.checkbox.setChecked(
                    config_data["headcrop"]["active"]
                )
                self.view.body.headcrop_option_widget.number_selector_suboption_widget.number_selector._number_label.setText(
                    config_data["headcrop"]["value"]
                )

        except FileNotFoundError:
            with open(project_file_path, "w", encoding="utf-8") as f:
                json.dump("{}", f, indent=4)

    def delete_config(self, config_name):
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

                if config_name in configs:
                    del configs[config_name]
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
        self.view.body.illumina_clip_option_widget.adaptar_suboption.combo_box.clear()

        print(Path(__file__).name, "-", f"Available adapters: {adapters}")

        for adapter in adapters:
            self.view.body.illumina_clip_option_widget.adaptar_suboption.combo_box.addItem(
                adapter, userData=adapters_folder_path / adapter
            )
