import subprocess
from PySide6.QtCore import QThread, Signal


class CheckWorker(QThread):
    result = Signal(bool)

    def __init__(self, args: list):
        super().__init__()
        self.args = args

    def run(self):
        try:
            subprocess.run(self.args, capture_output=True, check=True)
            self.result.emit(True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            self.result.emit(False)
