from PySide6.QtCore import QObject, Signal
from typing import Optional


class FileScannerWorker(QObject):
    finished = Signal(list)  # emitirá lista de rutas (strings)
    error = Signal(str)

    def __init__(self, fltr: Optional[str] = None):
        super().__init__()
        self.fltr = fltr

    def run(self):
        try:
            # importa aquí para evitar overhead en import global si no se usa
            from utils import (
                get_source_files_paths,
                get_trimmed_files_paths,
                get_sorted_files_paths,
                get_krakened_files_paths,
            )

            source_files = get_source_files_paths()
            trimmed_files = get_trimmed_files_paths()
            sorted_files = get_sorted_files_paths()
            krakened_files = get_krakened_files_paths()

            if self.fltr == "Recortados":
                files = trimmed_files
            elif self.fltr == "Ordenados":
                files = sorted_files
            elif self.fltr == "Taxonomizado":
                files = krakened_files
            else:
                files = source_files + trimmed_files + sorted_files + krakened_files

            # convertir a strings evita problemas con tipos Qt al pasar por señales
            files_str = [p.as_posix() for p in files if p.exists()]
            self.finished.emit(files_str)
        except Exception as e:
            self.error.emit(str(e))
