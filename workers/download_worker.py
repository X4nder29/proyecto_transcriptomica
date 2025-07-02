import os
import re
import requests
from pathlib import Path
from urllib.parse import urlparse
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget


class DownloadThread(QThread):
    progress_changed = Signal(int)
    file_name_signal = Signal(str)
    finished_signal = Signal(bool, str)

    def __init__(self, url: str, dest_folder: str, parent=None):
        super().__init__(parent)
        self.url = url
        self.dest_folder = dest_folder

    def run(self):
        try:
            resp = requests.get(self.url, stream=True, timeout=10)
            resp.raise_for_status()

            # Extraer nombre sugerido por Content-Disposition
            cd = resp.headers.get("content-disposition", "")
            filename = None
            if cd:
                m = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^\";]+)"?', cd)
                if m:
                    filename = m.group(1)
            if not filename:
                filename = (
                    os.path.basename(urlparse(self.url).path) or "downloaded.file"
                )
            self.file_name_signal.emit(filename)

            # Ruta completa de destino
            filepath = os.path.join(self.dest_folder, filename)

            # Preparar descarga
            total = int(resp.headers.get("content-length", 0))
            downloaded = 0
            chunk_size = 8192

            if total == 0:
                with open(filepath, "wb") as f:
                    f.write(resp.content)
                self.progress_changed.emit(100)
            else:
                with open(filepath, "wb") as f:
                    for chunk in resp.iter_content(chunk_size):
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        pct = int(downloaded * 100 / total)
                        self.progress_changed.emit(pct)

            self.finished_signal.emit(True, filepath)
        except Exception as e:
            self.finished_signal.emit(False, str(e))
