from PySide6.QtCore import QThread, Signal
from pathlib import Path
import requests
from urllib.parse import urlparse, unquote


class FilenameWorker(QThread):
    # Señal que emite el nombre de archivo (sin ruta)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, url: str, parent=None):
        super().__init__(parent)
        self.url = url

    def run(self):
        try:
            # 1) Petición HEAD para obtener las cabeceras
            resp = requests.head(self.url, allow_redirects=True, timeout=10)
            resp.raise_for_status()

            filename: Path | None = None

            # 2) Intentar extraer de Content-Disposition
            cd = resp.headers.get("content-disposition")
            if cd:
                parts = cd.split("filename=")
                if len(parts) > 1:
                    raw = parts[1].strip("\"; '")
                    filename = Path(unquote(raw))

            # 3) Si no vino en la cabecera, usar la URL
            if not filename or not filename.name:
                parsed = urlparse(self.url)
                # Path de la parte de la ruta de la URL y tomar el nombre
                filename = Path(unquote(parsed.path)).name
                filename = Path(filename)

            # 4) Emitir el nombre de archivo como cadena
            self.finished.emit(filename.name)

        except Exception as e:
            self.error.emit(str(e))
