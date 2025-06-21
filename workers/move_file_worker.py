import shutil
from PySide6.QtCore import QThread, Signal


class MoveFileWorker(QThread):
    finished = Signal(bool, str)  # éxito, mensaje

    def __init__(self, source, target):
        super().__init__()
        self.source = source
        self.target = target

    def run(self):
        try:
            shutil.move(self.source, self.target)
            self.finished.emit(True, "✅ Archivo movido correctamente")
        except Exception as e:
            self.finished.emit(False, f"❌ Error: {e}")
