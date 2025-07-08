import gzip
from pathlib import Path
from typing import Optional
from PySide6.QtCore import QThread, Signal


class UngzipWorker(QThread):
    # Señal que emite un entero [0–100]
    progress = Signal(int)
    # Señal que avisa cuando termina
    finished = Signal(object)
    # Señal que emite un mensaje de error
    error = Signal(str)

    def __init__(
        self,
        src_path: Path,
        dest_path: Optional[Path] = None,
        chunk_size: int = 1024 * 1024,
    ):
        super().__init__()
        # Aseguramos que sean objetos Path
        self.src_path = Path(src_path)
        self.dest_path = (
            Path(dest_path) if dest_path is not None else self.src_path.with_suffix("")
        )
        self.chunk_size = chunk_size

    def run(self):
        # Creamos directorio destino si no existe
        self.dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Obtenemos tamaño en bytes del .gz para el cálculo de porcentaje
        total_size = self.src_path.stat().st_size

        try:
            # Abrimos primero el archivo comprimido como fichero crudo…
            with self.src_path.open("rb") as raw:
                # …y lo envolvemos en GzipFile para descomprimir en streaming
                with gzip.GzipFile(fileobj=raw, mode="rb") as src, self.dest_path.open(
                    "wb"
                ) as dst:
                    while True:
                        chunk = src.read(self.chunk_size)
                        if not chunk:
                            break
                        dst.write(chunk)
                        # Medimos cuántos bytes del .gz hemos consumido
                        compressed_read = raw.tell()
                        pct = int(compressed_read * 100 / total_size)
                        self.progress.emit(pct)
        except Exception as e:
            # Aquí podrías emitir una señal de error si la defines
            print(f"Error al descomprimir: {e}")
            self.error.emit(str(e))
        finally:
            # Asegúrate de emitir 100% si no lo ha hecho
            self.progress.emit(100)
            self.finished.emit(self.dest_path)
