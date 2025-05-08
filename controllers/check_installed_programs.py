from PySide6.QtCore import QProcess, Signal, QObject, QStandardPaths, QDir, QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
import json


class CheckInstalledPrograms(QObject):

    APP_NAME = "transcriptohub"

    java_finished = Signal(str)
    trimmomatic_finished = Signal(str)

    app_data_path = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.AppDataLocation
    )
    
    app_data_dir = QDir(app_data_path)
    app_data_dir.mkpath(f"{APP_NAME}/programs")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.network_manager = QNetworkAccessManager()

    # checking

    def check_programs(self):
        self.check_java()
        self.check_trimmomatic()

    def check_java(self):
        process = QProcess(self)
        process.readyReadStandardOutput.connect(
            lambda: self.read_output(process, self.java_finished)
        )
        process.readyReadStandardError.connect(
            lambda: self.read_output(process, self.java_finished)
        )
        process.start("bash", ["-c", "java -version"])

    def check_trimmomatic(self):
        process = QProcess(self)
        process.readyReadStandardOutput.connect(
            lambda: self.read_output(process, self.trimmomatic_finished)
        )
        process.readyReadStandardError.connect(
            lambda: self.read_output(process, self.trimmomatic_finished)
        )
        process.start(
            "bash",
            [
                "-c",
                f"java -jar {self.app_data_path}/programs/trimmomatic-0.39.jar -version",
            ],
        )

    def read_output(self, process, finished_signal):
        output = process.readAllStandardOutput().data().decode()
        error = process.readAllStandardError().data().decode()
        finished_signal.emit(output if output else error)

    # downloading

    def download_trimmomatic(self):
        self.download_github_release("usadellab", "Trimmomatic", "trimmomatic-0.39.jar")
        self.check_trimmomatic()

    def download_github_release(self, repo_owner, repo_name, asset_name):
        """Descarga el release más reciente de un repositorio de GitHub.

        Args:
            repo_owner (str): Nombre del usuario u organización en GitHub.
            repo_name (str): Nombre del repositorio.
            asset_name (str): Nombre exacto del archivo a descargar dentro del release.
        """
        api_url = (
            f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        )
        request = QNetworkRequest(QUrl(api_url))
        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self._parse_github_release(reply, asset_name))

    def _parse_github_release(self, reply, asset_name):
        """Procesa la respuesta de GitHub y descarga el asset si se encuentra."""
        if reply.error():
            self.download_finished.emit(
                f"Error al obtener release: {reply.errorString()}"
            )
            return

        data = json.loads(reply.readAll().data().decode())
        assets = data.get("assets", [])

        for asset in assets:
            if asset["name"] == asset_name:
                self._download_file(asset["browser_download_url"])
                return

        self.download_finished.emit(
            f"No se encontró el archivo {asset_name} en el release."
        )

    def _download_file(self, url):
        """Descarga el archivo desde una URL."""
        request = QNetworkRequest(QUrl(url))
        reply = self.network_manager.get(request)
        reply.downloadProgress.connect(
            lambda bytes_received, bytes_total: self.download_progress.emit(
                int(100 * bytes_received / bytes_total)
            )
        )
        reply.finished.connect(lambda: self._save_file(reply, url.split("/")[-1]))

    def _save_file(self, reply, filename):
        """Guarda el archivo descargado."""
        if reply.error():
            self.download_finished.emit(f"Error en la descarga: {reply.errorString()}")
            return

        with open(filename, "wb") as file:
            file.write(reply.readAll().data())

        self.download_finished.emit(f"Descarga completada: {filename}")
