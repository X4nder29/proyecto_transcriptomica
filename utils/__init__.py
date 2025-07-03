from .settings import (
    get_current_workspace,
    set_current_workspace,
    clear_current_workspace,
    get_workspaces,
    add_new_workspace,
    remove_workspace,
    get_fastqc_executable_path_from_settings,
    set_fastqc_executable_path_in_settings,
    get_trimmomatic_executable_path_from_settings,
    set_trimmomatic_executable_path_in_settings,
    get_sortmerna_executable_path_from_settings,
    set_sortmerna_executable_path_in_settings,
    get_kraken2_database_folder_from_settings,
    set_kraken2_database_folder_in_settings,
)
from .utils import to_unc_path, center_window_on_screen, win_to_wsl, split_name
from .extract_fastqc_data import extract_fastqc_data
from .operation_modes import OperationModes