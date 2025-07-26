import os
import glob
from pathlib import Path
from PySide6.QtCore import QStandardPaths, QCoreApplication
from typing import Optional, Tuple
from views.main_window.panels.home_panel.widgets import current_workspace


QCoreApplication.setOrganizationName("Universidad Cooperativa de Colombia")
QCoreApplication.setOrganizationDomain("ucc.edu.co")
QCoreApplication.setApplicationName("TranscriptoHub")
QCoreApplication.setApplicationVersion("1.0.0")


def get_app_data_path() -> Path:
    """Get the path to the application data directory."""
    app_data_path = Path(
        QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    )
    if not app_data_path.exists():
        app_data_path.mkdir(parents=True, exist_ok=True)
        print(f"Created app data directory at: {app_data_path}")
    return app_data_path


"""
Funciones relacionadas con la ruta de los programas.
"""


def path_programs() -> Path:
    """Get the path to the programs directory."""
    programs_path = get_app_data_path() / "programs"
    if not programs_path.exists():
        programs_path.mkdir(parents=True, exist_ok=True)
        print(f"Created programs directory at: {programs_path}")
    return programs_path


"""
Funciones relacionadas con FastQC.
"""


def get_fastqc_folder_path() -> Optional[Path]:
    """
    Busca dentro de path_programs() una carpeta que en su nombre
    contenga 'fastqc' (case-insensitive) y devuelve su ruta completa.
    Si no la encuentra, devuelve None.
    """
    base_dir = path_programs()

    if not os.path.isdir(base_dir):
        return None

    for entry in base_dir.iterdir():
        if not entry.is_dir():
            continue

        if "fastqc" in entry.name.lower():
            return entry

    return None


def get_fastqc_file_path() -> Optional[Path]:
    """
    Busca dentro de path_programs() una carpeta que en su nombre
    contenga 'fastqc' (case-insensitive) y devuelve su ruta completa.
    Si no la encuentra, devuelve None.
    """
    base_dir = get_fastqc_folder_path()

    if base_dir is None:
        return None

    if not base_dir.is_dir():
        return None

    for entry in base_dir.glob("**/*"):
        if (
            entry.is_file()
            and "fastqc" in entry.name.lower()
            and entry.suffix == ".bat"
        ):
            return entry

    return None


def get_fastqc_output_folder_path_by_file(file_path: Path) -> Optional[Path]:
    """
    Obtiene la ruta de la carpeta de salida de FastQC para un archivo dado.
    Busca en el directorio de trabajo actual una carpeta llamada 'reports'
    y dentro de ella una carpeta que coincida con el nombre del archivo.
    """
    if not file_path.is_file():
        return None

    current_workspace_folder_path = get_current_workspace_folder_path()
    if current_workspace_folder_path is None:
        return None

    output_folder_path = current_workspace_folder_path / "reports" / file_path.stem
    print(f"Output folder path for FastQC: {output_folder_path}")
    if not output_folder_path.exists():
        return None

    return output_folder_path


"""
Funciones relacionadas con Trimmomatic.
"""


def get_trimmomatic_folder_path() -> Optional[Path]:
    """
    Busca dentro de path_programs() una carpeta que en su nombre
    contenga 'trimmomatic' (case-insensitive) y devuelve su ruta completa.
    Si no la encuentra, devuelve None.
    """
    base_dir = path_programs()

    if not base_dir.is_dir():
        return None

    for entry in base_dir.iterdir():
        if entry.is_dir() and "trimmomatic" in entry.as_posix().lower():
            return entry

    return None


def get_trimmomatic_jar_path() -> Optional[Path]:
    """
    Busca en el directorio <path_programs()>/trimmomatic
    cualquier archivo .jar que contenga 'trimmomatic' en su nombre
    y devuelve su ruta completa. Si no lo encuentra, devuelve None.
    """
    base_dir = get_trimmomatic_folder_path()
    if base_dir is None or not base_dir.is_dir():
        return None

    # Patrón para cualquier .jar que contenga 'trimmomatic' (case-insensitive)
    matches = list(base_dir.glob("*trimmomatic*.jar"))

    if not matches:
        return None

    return matches[0]


def get_trimmomatic_adapters_path() -> Optional[Path]:
    """Get the path to the Trimmomatic adapters file."""
    return get_trimmomatic_folder_path() / "adapters"


def get_trimmomatic_output_folder_path() -> Optional[Path]:
    """
    Obtiene la ruta de la carpeta 'trimmed' dentro del directorio de trabajo actual.
    Si no se ha establecido un directorio de trabajo, devuelve None.
    """
    current_workspace_folder_path = get_current_workspace_folder_path()

    if current_workspace_folder_path is None:
        return None

    output_folder_path = Path(current_workspace_folder_path) / "trimmed"

    if not output_folder_path.exists():
        output_folder_path.mkdir(parents=True, exist_ok=True)

    return output_folder_path


def get_trimmomatic_output_file_path(name: str) -> Optional[Path]:
    """
    Obtiene la ruta del archivo de salida de Trimmomatic.
    El archivo se nombra como 'trimmed_<número>.fastq' y se guarda en la carpeta 'trimmed'.
    Si no se puede determinar la ruta, devuelve None.
    """
    output_folder = get_trimmomatic_output_folder_path()

    if output_folder is None:
        return None

    output_file_count = len(list(output_folder.glob(f"{name}_trimmed_[0-9]*.fastq")))

    output_file_path = output_folder / f"{name}_trimmed_{output_file_count}.fastq"

    return output_file_path


def get_trimmomatic_output_1paired_file_path() -> Optional[Path]:
    """
    Obtiene la ruta del archivo de salida emparejado de Trimmomatic.
    El archivo se nombra como 'trimmed_<número>_paired.fastq' y se guarda en la carpeta 'trimmed'.
    Si no se puede determinar la ruta, devuelve None.
    """
    output_folder = get_trimmomatic_output_folder_path()

    if output_folder is None:
        return None

    output_file_count = len(list(output_folder.glob("trimmed_*_1paired.fastq")))

    output_file_path = output_folder / f"trimmed_{output_file_count}_paired.fastq"

    return output_file_path


def get_trimmomatic_output_2paired_file_path() -> Optional[Path]:
    """
    Obtiene la ruta del segundo archivo de salida emparejado de Trimmomatic.
    El archivo se nombra como 'trimmed_<número>_2paired.fastq' y se guarda en la carpeta 'trimmed'.
    Si no se puede determinar la ruta, devuelve None.
    """
    output_folder = get_trimmomatic_output_folder_path()

    if output_folder is None:
        return None

    output_file_count = len(list(output_folder.glob("trimmed_*_2paired.fastq")))

    output_file_path = output_folder / f"trimmed_{output_file_count}_2paired.fastq"

    return output_file_path


def get_trimmomatic_output_1unpaired_file_path() -> Optional[Path]:
    """
    Obtiene la ruta del archivo de salida no emparejado de Trimmomatic.
    El archivo se nombra como 'trimmed_<número>_unpaired.fastq' y se guarda en la carpeta 'trimmed'.
    Si no se puede determinar la ruta, devuelve None.
    """
    output_folder = get_trimmomatic_output_folder_path()

    if output_folder is None:
        return None

    output_file_count = len(list(output_folder.glob("trimmed_*_1unpaired.fastq")))

    output_file_path = output_folder / f"trimmed_{output_file_count}_unpaired.fastq"

    return output_file_path


def get_trimmomatic_output_2unpaired_file_path() -> Optional[Path]:
    """
    Obtiene la ruta del segundo archivo de salida no emparejado de Trimmomatic.
    El archivo se nombra como 'trimmed_<número>_2unpaired.fastq' y se guarda en la carpeta 'trimmed'.
    Si no se puede determinar la ruta, devuelve None.
    """
    output_folder = get_trimmomatic_output_folder_path()

    if output_folder is None:
        return None

    output_file_count = len(list(output_folder.glob("trimmed_*_2unpaired.fastq")))

    output_file_path = output_folder / f"trimmed_{output_file_count}_2unpaired.fastq"

    return output_file_path


"""
Funciones relacionadas con SortMeRNA.
"""


def get_sortmerna_folder_path() -> Optional[Path]:
    """
    Busca dentro de path_programs() una carpeta que en su nombre
    contenga 'sortmerna' (case-insensitive) y devuelve su ruta completa.
    Si no la encuentra, devuelve None.
    """
    base_dir = path_programs()

    if not base_dir.is_dir():
        return None

    for entry in base_dir.iterdir():
        if entry.is_dir() and "sortmerna" in entry.as_posix().lower():
            return entry

    return None


def get_sortmerna_executable_path() -> Optional[Path]:
    """
    Busca dentro de path_programs() un archivo que en su nombre
    contenga 'sortmerna' (case-insensitive) y devuelve su ruta completa.
    Si no lo encuentra, devuelve None.
    """
    base_dir = get_sortmerna_folder_path()

    if not base_dir or not base_dir.is_dir():
        return None

    for entry in base_dir.glob("**/*"):
        if entry.is_file() and "sortmerna" in entry.name.lower():
            return entry

    return None


def get_sortmerna_output_folder_path_from_workspace() -> Optional[Path]:
    current_workspace_folder_path = get_current_workspace_folder_path()

    if current_workspace_folder_path is None:
        return None

    output_folder_path = Path(current_workspace_folder_path) / "sorted"

    if not output_folder_path.exists():
        output_folder_path.mkdir(parents=True, exist_ok=True)

    return output_folder_path


def get_sortmerna_output_folder_path(name: str) -> Optional[Path]:
    """
    Obtiene la ruta de la carpeta de salida de SortMeRNA para un archivo dado.
    Busca en el directorio de trabajo actual una carpeta llamada 'sorted'
    y dentro de ella una carpeta que coincida con el nombre del archivo.
    """
    output_folder = get_sortmerna_output_folder_path_from_workspace()

    if output_folder is None:
        return None

    output_folder_count = len(
        list(
            filter(
                lambda x: x.is_dir() and any(x.iterdir()),
                list(output_folder.glob(f"{name}_sorted_[0-9]*")),
            )
        )
    )

    output_folder_path = output_folder / f"{name}_sorted_{output_folder_count}"

    if not output_folder_path.exists():
        output_folder_path.mkdir(parents=True, exist_ok=True)

    return output_folder_path


def get_sortmerna_databases_files() -> list[Path]:
    """
    Obtiene una lista de bases de datos de SortMeRNA.
    Cada base de datos es una tupla que contiene el nombre y la ruta de la base de datos.
    """
    databases_folder = get_sortmerna_databases_folder_path()

    if not databases_folder or not databases_folder.is_dir():
        return None

    databases = []
    for db_file in databases_folder.glob("*.fasta"):
        if db_file.is_file():
            databases.append(db_file)

    return databases


def get_sortmerna_databases_folder_path() -> Path:
    """
    Busca dentro de path_programs() una carpeta que en su nombre
    contenga 'sortmerna' (case-insensitive) y devuelve su ruta completa.
    Si no la encuentra, devuelve None.
    """
    base_dir = get_app_data_path()

    folder = base_dir / "Databases" / "SortMeRNA"

    if not folder.is_dir():
        folder.mkdir(parents=True, exist_ok=True)

    return folder


# saved configs
def get_sortmerna_saved_configs() -> Optional[list[str]]:
    """
    Obtiene una lista de configuraciones guardadas de SortMeRNA.
    Cada configuración es una tupla que contiene el nombre de la base de datos
    y la ruta de la base de datos.
    """
    project_file_path = get_project_file_path()

    if not project_file_path:
        return None

    import json

    try:
        with open(project_file_path, "r") as f:
            data = json.load(f)
            configs = data.get("sortmerna_configs", {})
            return [key for key in configs.keys()]
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def set_sortmerna_saved_config(name: str, data: dict) -> None:
    """
    Guarda una configuración de SortMeRNA en el archivo de proyecto.
    """
    project_file_path = get_project_file_path()

    if not project_file_path:
        return

    import json

    try:
        with open(project_file_path, "r") as f:
            project_file_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        project_file_data = {}

    if "sortmerna_configs" not in project_file_data:
        project_file_data["sortmerna_configs"] = {}

    project_file_data["sortmerna_configs"][name] = data

    with open(project_file_path, "w") as f:
        json.dump(project_file_data, f, indent=4)


def get_sortmerna_saved_config(name: str) -> Optional[dict]:
    """
    Obtiene una configuración guardada de SortMeRNA del archivo de proyecto.
    Si no se encuentra la configuración, devuelve None.
    """
    project_file_path = get_project_file_path()

    if not project_file_path:
        return None

    import json

    try:
        with open(project_file_path, "r") as f:
            data = json.load(f)
            if "sortmerna_configs" in data and name in data["sortmerna_configs"]:
                return data["sortmerna_configs"][name]
            else:
                return None
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def remove_sortmerna_saved_config(name: str) -> None:
    """
    Elimina una configuración guardada de SortMeRNA del archivo de proyecto.
    """
    project_file_path = get_project_file_path()

    if not project_file_path:
        return

    import json

    try:
        with open(project_file_path, "r") as f:
            data = json.load(f)
            if "sortmerna_configs" in data and name in data["sortmerna_configs"]:
                del data["sortmerna_configs"][name]

        with open(project_file_path, "w") as f:
            json.dump(data, f, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        pass


"""
Funciones relacionadas con Kraken2.
"""


def get_kraken2_databases_folder_path() -> Path:
    """
    Busca dentro de path_programs() una carpeta que en su nombre
    contenga 'kraken2' (case-insensitive) y devuelve su ruta completa.
    Si no la encuentra, devuelve None.
    """
    base_dir = get_app_data_path()

    folder = base_dir / "Databases" / "Kraken2"

    if not folder.is_dir():
        folder.mkdir(parents=True, exist_ok=True)

    return folder


def get_kraken2_database_folders() -> list[Path]:
    """
    Obtiene una lista de todas las carpetas de bases de datos de Kraken2
    dentro del directorio de bases de datos de Kraken2.
    """
    base_dir = get_kraken2_databases_folder_path()

    if not base_dir.is_dir():
        return []

    database_folders = []

    for entry in base_dir.iterdir():
        if not entry.is_dir():
            continue

        # Filtrar solo las carpetas que contienen bases de datos de Kraken2
        if any(entry.glob("*.k2d")):
            database_folders.append(entry)

    return database_folders


def get_kraken2_output_folder_path() -> Optional[Path]:
    """
    Obtiene la ruta de la carpeta 'reports' dentro del directorio de trabajo actual.
    Si no se ha establecido un directorio de trabajo, devuelve None.
    """
    workspace_path = get_current_workspace_folder_path()

    if not workspace_path:
        return None

    output_folder_path = Path(workspace_path) / "krakened"
    if not output_folder_path.exists():
        output_folder_path.mkdir(parents=True, exist_ok=True)

    return output_folder_path


def get_kraken2_saved_configs() -> Optional[list[str]]:
    """
    Obtiene una lista de configuraciones guardadas de Kraken2.
    Cada configuración es una tupla que contiene el nombre de la base de datos
    y la ruta de la base de datos.
    """
    project_file_path = get_project_file_path()

    if not project_file_path:
        return None

    import json

    try:
        with open(project_file_path, "r") as f:
            data = json.load(f)
            configs = data.get("kraken2_configs", {})
            return [key for key in configs.keys()]
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def set_kraken2_saved_config(name: str, data: dict) -> None:
    """
    Guarda una configuración de Kraken2 en el archivo de proyecto.
    """
    project_file_path = get_project_file_path()

    if not project_file_path:
        return

    import json

    try:
        with open(project_file_path, "r") as f:
            project_file_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        project_file_data = {}

    if "kraken2_configs" not in project_file_data:
        project_file_data["kraken2_configs"] = {}

    project_file_data["kraken2_configs"][name] = data

    with open(project_file_path, "w") as f:
        json.dump(project_file_data, f)


def get_kraken2_saved_config(name: str) -> Optional[dict]:
    """
    Obtiene una configuración guardada de Kraken2 del archivo de proyecto.
    Si no se encuentra la configuración, devuelve None.
    """
    project_file_path = get_project_file_path()

    if not project_file_path:
        return None

    import json

    try:
        with open(project_file_path, "r") as f:
            data = json.load(f)
            if "kraken2_configs" in data and name in data["kraken2_configs"]:
                return data["kraken2_configs"][name]
            else:
                return None
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def remove_kraken2_saved_config(name: str) -> None:
    """
    Elimina una configuración guardada de Kraken2 del archivo de proyecto.
    """
    project_file_path = get_project_file_path()

    if not project_file_path:
        return

    import json

    try:
        with open(project_file_path, "r") as f:
            data = json.load(f)
            if "kraken2_configs" in data and name in data["kraken2_configs"]:
                del data["kraken2_configs"][name]

        with open(project_file_path, "w") as f:
            json.dump(data, f, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        pass


"""
Funciones relacionadas con el directorio de trabajo actual.
"""


def get_current_workspace_folder_path() -> Optional[Path]:
    """
    Obtiene la ruta del directorio de trabajo actual.
    Si no se ha establecido, devuelve None.
    """
    from .settings import settings

    current_workspace = settings.value("current_workspace", None)
    if current_workspace:
        return Path(current_workspace)
    else:
        return None


def get_current_workspace_source_folder_path() -> Path:
    """
    Obtiene la ruta de la carpeta 'source' dentro del directorio de trabajo actual.
    Si no se ha establecido un directorio de trabajo, devuelve None.
    """
    workspace_path = get_current_workspace_folder_path()
    if not workspace_path:
        return None

    source_folder_path = Path(workspace_path) / "source"

    if not source_folder_path.exists():
        source_folder_path.mkdir(parents=True, exist_ok=True)
        print(f"Created source folder at: {source_folder_path}")

    return source_folder_path


def get_files_in_workspace_folder() -> list[Path]:
    """
    Obtiene una lista de rutas a archivos de secuencias que estén
    dentro de las carpetas 'trimmed' y 'sorted' del workspace actual.
    Las extensiones válidas son:
      - .fastq
      - .fastq.gz
      - .fasta
      - .fasta.gz

    Si no se ha establecido un directorio de trabajo, devuelve una lista vacía.
    """
    workspace_path = get_current_workspace_folder_path()
    if not workspace_path:
        return []

    # Extensiones que queremos capturar
    exts = ["fastq", "fastq.gz", "fasta", "fasta.gz", "fa", "fq"]

    collected: list[Path] = []
    for ext in exts:
        # Carpeta 'source'
        source_path = Path(workspace_path) / "source"
        if source_path.is_dir():
            collected.extend(source_path.glob("**/*." + ext))

        # Carpeta 'trimmed'
        trimmed_path = Path(workspace_path) / "trimmed"
        if trimmed_path.is_dir():
            collected.extend(trimmed_path.glob("**/*." + ext))

        # Carpeta 'sorted'
        sorted_path = Path(workspace_path) / "sorted"
        if sorted_path.is_dir():
            collected.extend(sorted_path.glob("**/*." + ext))

    # Devolver la lista ordenada para consistencia
    return sorted(collected)


def get_project_file_path() -> Optional[str]:
    """
    Obtiene la ruta del archivo de proyecto actual.
    Si no se ha establecido, devuelve None.
    """
    current_workspace = get_current_workspace_folder_path()

    if not current_workspace:
        return None

    project_file = os.path.join(current_workspace, "project.json")

    if os.path.exists(project_file):
        return project_file
    else:
        return None


def get_source_files_paths() -> list[Path]:
    """
    Obtiene una lista de rutas a los archivos de secuencias fuente
    que estén dentro del directorio de trabajo actual.
    Las extensiones válidas son:
      - .fastq
      - .fastq.gz
      - .fasta
      - .fasta.gz

    Si no se ha establecido un directorio de trabajo, devuelve una lista vacía.
    """
    workspace_path = get_current_workspace_folder_path()
    if not workspace_path:
        return []

    # Extensiones que queremos capturar
    exts = ["fastq", "fastq.gz", "fasta", "fasta.gz", "fa", "fq"]

    collected: list[Path] = []

    for ext in exts:
        path = Path(workspace_path) / "source"

        if not path.is_dir():
            continue

        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            continue

        collected.extend(path.glob("**/*." + ext))

    # Devolver la lista ordenada para consistencia
    return sorted(collected)


def get_trimmed_files_paths() -> list[Path]:
    """
    Obtiene una lista de rutas a los archivos de secuencias recortadas
    que estén dentro del directorio de trabajo actual.
    Las extensiones válidas son:
      - .fastq
      - .fastq.gz
      - .fasta
      - .fasta.gz

    Si no se ha establecido un directorio de trabajo, devuelve una lista vacía.
    """
    workspace_path = get_current_workspace_folder_path()
    if not workspace_path:
        return []

    # Extensiones que queremos capturar
    exts = ["fastq", "fastq.gz", "fasta", "fasta.gz"]

    collected: list[Path] = []
    path = Path(workspace_path) / "trimmed"

    if not path.is_dir():
        return collected

    for ext in exts:
        collected.extend(path.glob("**/*." + ext))

    # Devolver la lista ordenada para consistencia
    return sorted(collected)


def get_sorted_files_paths() -> list[Path]:
    """
    Obtiene una lista de rutas a los archivos de secuencias ordenadas
    que estén dentro del directorio de trabajo actual.
    Las extensiones válidas son:
      - .fastq
      - .fastq.gz
      - .fasta
      - .fasta.gz
      - .fq
      - .fa

    Si no se ha establecido un directorio de trabajo, devuelve una lista vacía.
    """
    workspace_path = get_current_workspace_folder_path()
    if not workspace_path:
        return []

    # Extensiones que queremos capturar
    exts = ["fastq", "fastq.gz", "fasta", "fasta.gz", "fa", "fq"]

    collected: list[Path] = []
    path = Path(workspace_path) / "sorted"

    if not path.is_dir():
        return collected

    for ext in exts:
        collected.extend(path.glob("**/*." + ext))

    # Devolver la lista ordenada para consistencia
    return sorted(collected)


def get_sorted_folders_paths() -> list[Path]:
    """
    Obtiene una lista de rutas a las carpetas de archivos ordenados
    que estén dentro del directorio de trabajo actual.
    Las carpetas deben contener archivos con extensiones válidas:
      - .fastq
      - .fastq.gz
      - .fasta
      - .fasta.gz

    Si no se ha establecido un directorio de trabajo, devuelve una lista vacía.
    """
    workspace_path = get_current_workspace_folder_path()
    if not workspace_path:
        return []

    collected: list[Path] = []
    path = Path(workspace_path) / "sorted"

    if not path.is_dir():
        return collected

    for entry in path.iterdir():
        if entry.is_dir() and any(entry.glob("**/*")):
            collected.append(entry)

    return sorted(collected)


def get_krakened_files_paths() -> list[Path]:
    """
    Obtiene una lista de rutas a los reportes procesadas por Kraken2 y krona
    que estén dentro del directorio de trabajo actual.
    Las extensiones válidas son:
      - .html

    Si no se ha establecido un directorio de trabajo, devuelve una lista vacía.
    """
    workspace_path = get_current_workspace_folder_path()
    if not workspace_path:
        return []

    # Extensiones que queremos capturar
    exts = ["html", "txt"]

    collected: list[Path] = []
    path = get_kraken2_output_folder_path()

    if not path or not path.is_dir():
        return collected

    for ext in exts:
        collected.extend(path.glob("**/*." + ext))

    # Devolver la lista ordenada para consistencia
    return sorted(collected)
