import os
from PySide6.QtCore import QStandardPaths, QCoreApplication


QCoreApplication.setOrganizationName("Universidad Cooperativa de Colombia")
QCoreApplication.setOrganizationDomain("ucc.edu.co")
QCoreApplication.setApplicationName("Transcripohub")
QCoreApplication.setApplicationVersion("1.0.0")


def get_app_data_path() -> str:
    """Get the path to the application data directory."""
    app_data_path = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    if not os.path.exists(app_data_path):
        os.makedirs(app_data_path, exist_ok=True)
        print(f"Created app data directory at: {app_data_path}")
    return app_data_path


"""
Funciones relacionadas con la ruta de los programas.
"""


def path_programs() -> str:
    """Get the path to the programs directory."""
    programs_path = os.path.join(get_app_data_path(), "programs")
    if not os.path.exists(programs_path):
        os.makedirs(programs_path, exist_ok=True)
        print(f"Created programs directory at: {programs_path}")
    return programs_path


"""
Funciones relacionadas con FastQC.
"""


def get_fastqc_folder_path() -> str:
    """
    Busca dentro de path_programs() una carpeta que en su nombre
    contenga 'fastqc' (case-insensitive) y devuelve su ruta completa.
    Si no la encuentra, devuelve None.
    """
    base_dir = path_programs()

    if not os.path.isdir(base_dir):
        return None

    for entry in os.listdir(base_dir):
        full_path = os.path.join(base_dir, entry)
        if os.path.isdir(full_path) and "fastqc" in entry.lower():
            return full_path

    return None


def get_fastqc_file_path() -> Optional[str]:
    """
    Busca dentro de path_programs() una carpeta que en su nombre
    contenga 'fastqc' (case-insensitive) y devuelve su ruta completa.
    Si no la encuentra, devuelve None.
    """
    base_dir = get_fastqc_folder_path()

    if not os.path.isdir(base_dir):
        return None

    for entry in os.listdir(base_dir):
        full_path = os.path.join(base_dir, entry)
        if "run_fastqc.bat" in entry.lower():
            return full_path

    return None

