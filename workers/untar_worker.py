import tarfile
import os
from pathlib import Path
from PySide6.QtCore import QThread, Signal


class UntarWorker(QThread):
    # Señal que emite el porcentaje de progreso (0–100)
    progress_changed = Signal(int)
    # Señal que emite cuando termina (sin errores)
    finished = Signal(object)
    # Señal que emite en caso de error, con el mensaje
    error = Signal(str)

    def __init__(self, tar_path: Path, dest_path: Path, parent=None):
        super().__init__(parent)
        self.tar_path = tar_path
        self.dest_path = dest_path

    def run(self):
        try:
            # Abre el .tar (funciona con .tar, .tar.gz, .tar.bz2, ...)
            with tarfile.open(self.tar_path, "r:*") as tf:
                members = tf.getmembers()
                total = len(members)
                if total == 0:
                    # Nada que extraer
                    self.progress_changed.emit(100)
                    self.finished.emit()
                    return

                # Asegurarse de que existe el destino
                os.makedirs(self.dest_path, exist_ok=True)

                for idx, member in enumerate(members, start=1):
                    # Extrae este miembro
                    tf.extract(member, path=self.dest_path)
                    # Calcula y emite progreso
                    percent = int((idx / total) * 100)
                    self.progress_changed.emit(percent)

                # Asegurar 100% al final
                self.progress_changed.emit(100)
                self.finished.emit(self.dest_path)

        except Exception as e:
            # En caso de cualquier fallo, emitimos la señal de error
            self.error.emit(str(e))
