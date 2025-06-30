from pathlib import Path
from typing import Optional
from PySide6.QtCore import QDir, QSettings

from utils.paths import get_app_data_path


settings_file = QDir(get_app_data_path()).filePath("transcriptohub.ini")

settings = QSettings(settings_file, QSettings.IniFormat)


def get_current_workspace() -> Optional[Path]:
    """
    Get the current workspace path from the settings.
    """
    current_workspace = settings.value("current_workspace", "")

    if not isinstance(current_workspace, str):
        current_workspace = ""

    return Path(current_workspace) if current_workspace else None


def set_current_workspace(workspace_path: Path):
    """
    Set the current workspace in the settings.
    """
    if not isinstance(workspace_path, Path):
        raise ValueError("workspace_path must be a Path object")

    if not workspace_path.exists():
        raise FileNotFoundError(f"Workspace path {workspace_path} does not exist")

    settings.setValue("current_workspace", workspace_path.as_posix())


def clear_current_workspace():
    """
    Clear the current workspace in the settings.
    """
    settings.setValue("current_workspace", "")


def get_workspaces() -> list[Path]:
    """
    Get the list of workspaces from the settings.
    """
    workspaces: list = settings.value("workspaces", [], list)

    if not isinstance(workspaces, list):
        workspaces = []

    return [Path(workspace) for workspace in workspaces]


def add_new_workspace(workspace_path: Path):
    """
    Add a new workspace to the settings.
    """
    workspaces: list = settings.value("workspaces", [], list)

    if not isinstance(workspaces, list):
        workspaces = []

    if not workspace_path.as_posix() in workspaces:
        workspaces.append(workspace_path.as_posix())

    settings.setValue("workspaces", workspaces)


def remove_workspace(workspace_path: Path):
    """
    Remove a workspace from the settings.
    """
    workspaces = settings.value("workspaces", [], list)

    if not isinstance(workspaces, list):
        workspaces = []

    if workspace_path.as_posix() in workspaces:
        workspaces.remove(workspace_path.as_posix())

    settings.setValue("workspaces", [] if workspaces == [] else workspaces)


# programs


# get fastqc executable path
def get_fastqc_executable_path_from_settings() -> Optional[Path]:
    """
    Get the FastQC executable path from the settings.
    """
    fastqc_executable = settings.value("fastqc_executable", "")
    if not isinstance(fastqc_executable, str):
        fastqc_executable = ""
    return Path(fastqc_executable) if fastqc_executable else None


# set fastqc executable path
def set_fastqc_executable_path_in_settings(path: Path):
    """
    Set the FastQC executable path in the settings.
    """
    if not isinstance(path, Path):
        raise ValueError("path must be a Path object")
    if not path.exists():
        raise FileNotFoundError(f"FastQC executable path {path} does not exist")
    settings.setValue("fastqc_executable", path.as_posix())


# get trimmomatic executable path
def get_trimmomatic_executable_path_from_settings() -> Optional[Path]:
    """
    Get the Trimmomatic executable path from the settings.
    """
    trimmomatic_executable = settings.value("trimmomatic_executable", "")
    if not isinstance(trimmomatic_executable, str):
        trimmomatic_executable = ""
    return Path(trimmomatic_executable) if trimmomatic_executable else None


# set trimmomatic executable path
def set_trimmomatic_executable_path_in_settings(path: Path):
    """
    Set the Trimmomatic executable path in the settings.
    """
    if not isinstance(path, Path):
        raise ValueError("path must be a Path object")
    if not path.exists():
        raise FileNotFoundError(f"Trimmomatic executable path {path} does not exist")
    settings.setValue("trimmomatic_executable", path.as_posix())


# get sortmerna executable path
def get_sortmerna_executable_path_from_settings() -> Optional[Path]:
    """
    Get the SortMeRNA executable path from the settings.
    """
    sortmerna_executable = settings.value("sortmerna_executable", "")
    if not isinstance(sortmerna_executable, str):
        sortmerna_executable = ""
    return Path(sortmerna_executable) if sortmerna_executable else None


# set sortmerna executable path
def set_sortmerna_executable_path_in_settings(path: Path):
    """
    Set the SortMeRNA executable path in the settings.
    """
    if not isinstance(path, Path):
        raise ValueError("path must be a Path object")

    if not path.exists():
        raise FileNotFoundError(f"SortMeRNA executable path {path} does not exist")

    settings.setValue("sortmerna_executable", path.as_posix())


# get kraken2 database folder path
def get_kraken2_database_folder_from_settings() -> Optional[Path]:
    """
    Get the Kraken2 database folder path from the settings.
    """
    kraken2_database = settings.value("kraken2_database", "", str)

    if not isinstance(kraken2_database, str):
        kraken2_database = ""

    return Path(kraken2_database) if kraken2_database else None


# set kraken2 database folder path
def set_kraken2_database_folder_in_settings(path: Path):
    """
    Set the Kraken2 database folder path in the settings.
    """
    if not isinstance(path, Path):
        raise ValueError("path must be a Path object")

    if not path.exists():
        raise FileNotFoundError(f"Kraken2 database folder path {path} does not exist")

    settings.setValue("kraken2_database", path.as_posix())
