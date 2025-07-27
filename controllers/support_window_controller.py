from typing import Optional
from pathlib import Path
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt, QFile, QIODevice, QTextStream
from views.support_window import SupportWindow


class SupportWindowController:

    manual_content = {
        "Bienvenida": ":/manual/welcome.html",
        "Inicio": ":/manual/home.html",
        "FastQC": ":/manual/fastqc.html",
        "Trimmomatic": ":/manual/trimmomatic.html",
        "SortMeRNA": ":/manual/sortmerna.html",
        "Kraken2": ":/manual/kraken2.html",
        "Configuraciones": ":/manual/settings.html",
        "WSL": ":/manual/wsl.html",
    }

    def __init__(self, view: SupportWindow, initial_section: Optional[str] = None):
        self.view = view
        self.initial_section = initial_section

        self.view.sidebar.currentItemChanged.connect(self._show_content)

        self._setup_sidebar()
        self._setup_initial_content()

    def _setup_sidebar(self):
        for section in self.manual_content:
            self.view.sidebar.addItem(section)

    def _setup_initial_content(self):
        if self.initial_section and self.initial_section in self.manual_content:
            item = self.view.sidebar.findItems(
                self.initial_section, Qt.MatchFlag.MatchExactly
            )
            if item:
                self.view.sidebar.setCurrentItem(item[0])
        else:
            self.view.sidebar.setCurrentRow(0)

    def _show_content(self, item: QListWidgetItem):
        titulo = item.text()

        """ md = 

        self.view.content.viewer.setMarkdown(html) """

        f = QFile(self.manual_content.get(titulo, ":/manual/no_content.md"))
        if not f.open(QIODevice.ReadOnly | QIODevice.Text):
            html = "<p>No se pudo leer el manual.</p>"
        else:
            stream = QTextStream(f)
            markdown_text = stream.readAll()
            f.close()
            html = markdown_text

        self.view.content.viewer.setHtml(html)

        print(f"{Path(__file__).name}", "-", f"Mostrando contenido para: {titulo}")
