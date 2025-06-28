import os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QCursor

def to_unc_path(path):
    """
    Convierte una ruta local de Windows a formato UNC utilizando el nombre del host local.
    Por ejemplo: 'C:\\Usuarios\\Juan\\archivo.txt' -> '\\\\localhost\\C$\\Usuarios\\Juan\\archivo.txt'
    """
    # Normaliza la ruta para asegurar que los separadores sean correctos
    normalized_path = os.path.normpath(path)

    # Divide la ruta en unidad y el resto del camino
    disk_drive, remaining_path = os.path.splitdrive(normalized_path)

    # Extrae la letra de la unidad sin el carácter ':'
    drive_letter = disk_drive.rstrip(":")

    # Construye la ruta UNC utilizando el nombre del host local y la unidad compartida
    unc_path = f"\\\\localhost\\{drive_letter}$\\{remaining_path.lstrip(os.sep)}"

    return unc_path

def center_window_on_screen(window, screen=None):
    """
    Centers the given window on the specified screen.
    If no screen is provided, it uses the screen where the mouse cursor is.
    """
    if screen is None:
        screen = QApplication.screenAt(QCursor.pos())
        if screen is None:
            screen = QApplication.primaryScreen()

    screen_geometry = screen.availableGeometry()
    screen_center = screen_geometry.center()

    window_geometry = window.frameGeometry()
    window_geometry.moveCenter(screen_center)
    window.move(window_geometry.topLeft())


def win_to_wsl(p: Path) -> Path:
    """
    Convierte una ruta Windows (ej. C:\\Users\\…)
    en su equivalente WSL (/mnt/c/…).
    """
    # Obtiene la letra de unidad (p.drive es 'C:' en tu caso)
    drive = p.drive.rstrip(":").lower()      # → 'c'
    # p.anchor es 'C:\\' en WindowsPath
    rel   = p.relative_to(p.anchor)          # → Path('Users/Alexander/Desktop/Test 1/source/2CP_…')
    return Path("/mnt") / drive / rel