from concurrent.futures import thread
import os
from PySide6.QtCore import QProcess
from views.main_window.panels.trimmomatic_panel import TrimmomaticPanel


class TrimmomaticPanelController:
    def __init__(self, view: TrimmomaticPanel):
        self.view = view
        self.process = QProcess()

        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_error)

        self.view.head.play_button.clicked.connect(self.run_proccess)

    # run command

    def run_proccess(self):

        mode = self.view.body.mode_area.button_group.checkedButton().text()

        threads = self.view.body.threads_option.slider.value()

        phred = self.view.body.quality_scores_format_option.button_group.checkedId()

        # files for SE mode
        input_file_se = self.view.body.files_area_se.input_file_se.line_edit.text()
        output_file_se = self.view.body.files_area_se.output_file_se.line_edit.text()

        # files for PE mode
        input_file_pe1 = self.view.body.files_area_pe.output_file_2_pe.line_edit.text()
        input_file_pe2 = self.view.body.files_area_pe.input_file_2_pe.line_edit.text()
        output_file_paired1 = (
            self.view.body.files_area_pe.output_file_1_pe.line_edit.text()
        )
        output_file_paired2 = (
            self.view.body.files_area_pe.output_file_1_pe.line_edit.text()
        )
        output_file_unpaired1 = (
            self.view.body.files_area_pe.output_file_2_pe.line_edit.text()
        )
        output_file_unpaired2 = (
            self.view.body.files_area_pe.output_file_2_pe.line_edit.text()
        )

        adapter = self.view.body.illumina_clip_option.adapter_options.currentText()
        seed_mismatches = (
            self.view.body.illumina_clip_option.seed_mismatches_input._number_label.text()
        )
        palindrome_clip_threshold = (
            self.view.body.illumina_clip_option.palindrome_clip_threshold_input._number_label.text()
        )
        simple_clip_threshold = (
            self.view.body.illumina_clip_option.simple_clip_threshold_input._number_label.text()
        )
        leading = self.view.body.leading_option.number_selector._number_label.text()
        trailing = self.view.body.trailing_option.number_selector._number_label.text()
        window_size = (
            self.view.body.slidingwindow_option.window_size_selector._number_label.text()
        )
        quality_threshold = (
            self.view.body.slidingwindow_option.quality_threshold_selector._number_label.text()
        )
        minlen = self.view.body.minlen_option.number_selector._number_label.text()
        crop = self.view.body.crop_option.number_selector._number_label.text()

        adapter = ".\\adapters\\TruSeq3_SE.fa"

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

        """ self.process.setWorkingDirectory("D:\\projects_ucc\\proyecto_transcriptomica\\programs\\trimmomatic_0.39\\") """
        self.process.start(
            "java",
            [
                "-jar",
                "D:\\projects_ucc\\proyecto_transcriptomica\\programs\\trimmomatic_0.39\\trimmomatic_0.39.jar",
                mode,
                "-threads",
                str(threads),
                f"-phred{phred}",
                f"'{input_file_se}'",
                f"'{output_file_se}'",
                f'ILLUMINACLIP:"{adapter}":{seed_mismatches}:{palindrome_clip_threshold}:{simple_clip_threshold}',
                f"LEADING:{leading}",
                f"TRAILING:{trailing}",
                f"SLIDINGWINDOW:{window_size}:{quality_threshold}",
                f"MINLEN:{minlen}",
                f"CROP:{crop}",
            ],
        )

        """ (
            [
                f'"{input_file_se.replace("\\", "/")}"',
                f'"{output_file_se.replace("\\", "/")}"',
            ]
            if mode == "SE"
            else f'"{input_file_pe1}" "{input_file_pe2}" "{output_file_paired1}" "{output_file_unpaired1}" "{output_file_paired2}" "{output_file_unpaired2}"'
        ), """

    def read_output(self):
        print("output", self.process.readAllStandardOutput().data().decode())

    def read_error(self):
        print("error", self.process.readAllStandardError().data().decode())

    # save configs

    def load_configs(self):
        pass

    def save_configs(self):
        pass
