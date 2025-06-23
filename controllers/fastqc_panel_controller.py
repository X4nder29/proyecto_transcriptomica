import re
import json
from pathlib import Path
from typing import Optional, Tuple
from PySide6.QtCore import QProcess
from views import FilesWindow
from views.main_window.panels.fastqc_panel import FastqcPanel
from utils import (
    to_unc_path,
    extract_fastqc_data,
    get_current_workspace_folder_path,
    get_fastqc_file_path,
    get_fastqc_folder_path,
)


class FastQCPanelController:
    selected_input_file: Optional[Path] = None

    """
    Controller for handling FastQC panel operations.
    """

    def __init__(self, view: FastqcPanel):
        """
        Initializes the FastQCPanelController with a FastQC service.

        :param fastqc_service: An instance of the FastQC service.
        """
        self.view = view

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.on_stdout)
        self.process.readyReadStandardError.connect(self.ou_stderr)
        self.process.finished.connect(self.on_finished)

        self.view.body.input_file_widget.select_file_button.clicked.connect(
            self.open_files_window
        )
        self.view.body.report_generation_widget.cancel_button.clicked.connect(
            self.cancel_report_generation
        )
        self.view.head.cli_push_button.clicked.connect(self._open_cli_dialog)

    def _open_cli_dialog(self):
        if self.selected_input_file is None:
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self.view,
                "No file selected",
                "Please select a file to generate a report.",
            )
            return

        command = self._generate_command(self.selected_input_file)

        from views.widgets import CliDialog

        cli_dialog = CliDialog(self.view)
        cli_dialog.set_command(command[0] + " " + " ".join(command[1]))
        cli_dialog.show()

    def check_existing_report(self, file: Path):

        print(f"Checking report for {file}...")

        workspace = get_current_workspace_folder_path()

        if not workspace:
            print("No workspace set. Please set a workspace first.")
            return

        if not file:
            print("No file path provided.")
            return

        report_path = Path(workspace) / "reports" / file.stem

        if report_path.exists() and report_path.is_dir() and any(report_path.iterdir()):
            print(Path(__file__).name, "-", f"Report already exists for {file}.")

            self.view.body.main_layout.removeWidget(self.view.body.report_content_area)
            self.view.body.main_layout.addWidget(
                self.view.body.report_content_area, 1, 1, 2, 1
            )
            self.view.body.basic_statistics_report_widget.setVisible(True)
            self.view.body.report_content_area.setCurrentIndex(2)

            self.get_fastqc_results(report_path)

        else:
            print(f"No report found for {file}. Generating report...")
            self.view.body.basic_statistics_report_widget.setVisible(False)
            self.view.body.main_layout.removeWidget(self.view.body.report_content_area)
            self.view.body.main_layout.addWidget(
                self.view.body.report_content_area, 0, 1, 3, 1
            )
            self.view.body.report_content_area.setCurrentIndex(1)
            self.generate_report(file)

    def get_fastqc_results(self, report_path: Path):
        print(Path(__file__).name, "-", f"Getting FastQC results for {report_path}...")

        basic_statistics_path = report_path / "basic_statistics.json"
        if basic_statistics_path.exists():
            with basic_statistics_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                self.view.body.basic_statistics_report_widget.set_filename(
                    data[0]["Value"]
                )
                self.view.body.basic_statistics_report_widget.set_filetype(
                    data[1]["Value"]
                )
                self.view.body.basic_statistics_report_widget.set_encoding(
                    data[2]["Value"]
                )
                self.view.body.basic_statistics_report_widget.set_total_sequences(
                    data[3]["Value"]
                )
                self.view.body.basic_statistics_report_widget.set_sequences_flagged_as_poor_quality(
                    data[4]["Value"]
                )
                self.view.body.basic_statistics_report_widget.set_sequence_length(
                    data[5]["Value"]
                )
                self.view.body.basic_statistics_report_widget.set_percent_gc(
                    data[6]["Value"]
                )

        self.view.body.summary_list_widget.per_base_sequence_quality_push_button.setEnabled(
            True
        )
        self.view.body.summary_list_widget.per_sequence_quality_scores_push_button.setEnabled(
            True
        )
        self.view.body.summary_list_widget.per_base_sequence_content_push_button.setEnabled(
            True
        )
        self.view.body.summary_list_widget.per_sequence_gc_content_push_button.setEnabled(
            True
        )
        self.view.body.summary_list_widget.per_base_n_content.setEnabled(True)
        self.view.body.summary_list_widget.sequence_length_distribution_push_button.setEnabled(
            True
        )
        self.view.body.summary_list_widget.sequence_duplication_levels_push_button.setEnabled(
            True
        )
        self.view.body.summary_list_widget.overrepresented_sequences_push_button.setEnabled(
            True
        )
        self.view.body.summary_list_widget.adapter_content_push_button.setEnabled(True)

        self.view.body.summary_list_widget.per_base_sequence_quality_push_button.clicked.connect(
            lambda: self.show_report_chart(
                report_path / "per_base_sequence_quality.png"
            )
        )

        self.view.body.summary_list_widget.per_sequence_quality_scores_push_button.clicked.connect(
            lambda: self.show_report_chart(
                report_path / "per_sequence_quality_scores.png"
            )
        )

        self.view.body.summary_list_widget.per_base_sequence_content_push_button.clicked.connect(
            lambda: self.show_report_chart(
                report_path / "per_base_sequence_content.png"
            )
        )

        self.view.body.summary_list_widget.per_sequence_gc_content_push_button.clicked.connect(
            lambda: self.show_report_chart(report_path / "per_sequence_gc_content.png")
        )

        self.view.body.summary_list_widget.per_base_n_content.clicked.connect(
            lambda: self.show_report_chart(report_path / "per_base_n_content.png")
        )

        self.view.body.summary_list_widget.sequence_length_distribution_push_button.clicked.connect(
            lambda: self.show_report_chart(
                report_path / "sequence_length_distribution.png"
            )
        )

        self.view.body.summary_list_widget.sequence_duplication_levels_push_button.clicked.connect(
            lambda: self.show_report_chart(
                report_path / "sequence_duplication_levels.png"
            )
        )

        self.view.body.summary_list_widget.overrepresented_sequences_push_button.clicked.connect(
            lambda: self.show_report_table(
                report_path / "overrepresented_sequences.json"
            )
        )

        self.view.body.summary_list_widget.adapter_content_push_button.clicked.connect(
            lambda: self.show_report_chart(report_path / "adapter_content.png")
        )

    def show_report_chart(self, chart_path: Path):
        if not chart_path.exists():
            self.view.body.report_content_area.setCurrentIndex(2)
            return

        self.view.body.report_chart_widget.set_chart(chart_path)
        self.view.body.report_content_area.setCurrentIndex(3)

    def show_report_table(self, table_data_path: Path):
        if not table_data_path.exists():
            self.view.body.report_content_area.setCurrentIndex(2)
            return

        with table_data_path.open("r", encoding="utf-8") as f:
            table_data = json.load(f)
            table_data = list(
                map(
                    lambda x: (
                        x["Sequence"],
                        x["Count"],
                        x["Percentage"],
                        x["Possible Source"],
                    ),
                    table_data,
                )
            )
            self.view.body.report_table_widget.set_table_data(table_data)
            self.view.body.report_content_area.setCurrentIndex(4)

    def _generate_command(self, file_path) -> Tuple[str, list[str]]:
        output_dir = (
            Path(get_current_workspace_folder_path()) / "reports" / Path(file_path).stem
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        arguments = [
            f"{file_path}",
            f"--outdir={to_unc_path(output_dir.as_posix())}",
        ]

        fastqc_file_path = get_fastqc_file_path()

        return (
            fastqc_file_path,
            arguments,
        )

    def generate_report(self, file_path):
        self.process.setWorkingDirectory(get_fastqc_folder_path())
        self.process.start(*self._generate_command(file_path))

    def on_stdout(self):
        """
        Reads the standard output from the FastQC process and updates the view.
        """
        if "Analysis complete" in self.process.readAllStandardOutput().data().decode():
            print(Path(__file__).name, "-", "FastQC analysis complete.")

    def ou_stderr(self):
        """
        Reads the standard error from the FastQC process and updates the view.
        """
        error = self.process.readAllStandardError().data().decode()
        """ print("FastQC output:", output) """
        progress_match = re.search(r"(\d+)%", error)

        if progress_match:
            progress = int(progress_match.group(1))
            self.view.body.report_generation_widget.progress_bar.setValue(progress)
            print(f"Progress: {progress}%")

    def on_finished(self, exit_code, exit_status):
        if exit_status == QProcess.ExitStatus.NormalExit and exit_code == 0:
            input_file_path = Path(self.process.arguments()[0])

            output_dir = (
                get_current_workspace_folder_path() / "reports" / input_file_path.stem
            )
            output_dir.mkdir(parents=True, exist_ok=True)

            input_file_path = input_file_path.with_name(input_file_path.stem + "_fastqc").with_suffix(".html")

            extract_fastqc_data(
                input_file_path.as_posix(),
                output_dir,
            )

            self.check_existing_report(
                Path(get_current_workspace_folder_path())
                / "reports"
                / Path(self.process.arguments()[0]).stem
            )

    def open_files_window(self):
        """Open the FilesWindow."""
        from controllers import FilesWindowController

        files_window = FilesWindow(parent=self.view)
        files_window_controller = FilesWindowController(files_window)
        result = files_window.exec_()

        if result == FilesWindow.Accepted:

            self._disable_summary_buttons()

            print("FilesWindow accepted")
            print(f"Selected file: {files_window_controller.selected_input_file}")

            self.selected_input_file = files_window_controller.selected_input_file

            self.view.body.input_file_widget.select_file_button.set_file(
                self.selected_input_file.stem, self.selected_input_file.as_posix()
            )

            self.check_existing_report(self.selected_input_file)
        else:
            self.view.body.input_file_widget.select_file_button.clear_file()
            print("FilesWindow rejected")

    def cancel_report_generation(self):
        """
        Cancels the report generation process.
        """
        if self.process.state() == QProcess.ProcessState.Running:
            self.process.kill()
            print(Path(__file__).name, "-", "Report generation cancelled.")
            self.view.body.basic_statistics_report_widget.setVisible(False)
            self.view.body.main_layout.removeWidget(self.view.body.report_content_area)
            self.view.body.main_layout.addWidget(
                self.view.body.report_content_area, 0, 1, 3, 1
            )
            self.view.body.report_content_area.setCurrentIndex(0)
            self.view.body.report_generation_widget.progress_bar.setValue(0)

        else:
            print(Path(__file__).name, "-", "No report generation process is running.")

    def _disable_summary_buttons(self):
        """
        Disables all summary buttons in the FastQC panel.
        """
        self.view.body.summary_list_widget.per_base_sequence_quality_push_button.setEnabled(
            False
        )
        self.view.body.summary_list_widget.per_base_sequence_quality_push_button.setChecked(
            False
        )

        self.view.body.summary_list_widget.per_sequence_quality_scores_push_button.setEnabled(
            False
        )
        self.view.body.summary_list_widget.per_sequence_quality_scores_push_button.setChecked(
            False
        )

        self.view.body.summary_list_widget.per_base_sequence_content_push_button.setEnabled(
            False
        )
        self.view.body.summary_list_widget.per_base_sequence_content_push_button.setChecked(
            False
        )

        self.view.body.summary_list_widget.per_sequence_gc_content_push_button.setEnabled(
            False
        )
        self.view.body.summary_list_widget.per_sequence_gc_content_push_button.setChecked(
            False
        )

        self.view.body.summary_list_widget.per_base_n_content.setEnabled(False)
        self.view.body.summary_list_widget.per_base_n_content.setChecked(False)

        self.view.body.summary_list_widget.sequence_length_distribution_push_button.setEnabled(
            False
        )
        self.view.body.summary_list_widget.sequence_length_distribution_push_button.setChecked(
            False
        )

        self.view.body.summary_list_widget.sequence_duplication_levels_push_button.setEnabled(
            False
        )
        self.view.body.summary_list_widget.sequence_duplication_levels_push_button.setChecked(
            False
        )

        self.view.body.summary_list_widget.overrepresented_sequences_push_button.setEnabled(
            False
        )
        self.view.body.summary_list_widget.overrepresented_sequences_push_button.setChecked(
            False
        )

        self.view.body.summary_list_widget.adapter_content_push_button.setEnabled(False)
        self.view.body.summary_list_widget.adapter_content_push_button.setChecked(False)
