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
    return app_data_path


def path_programs() -> str:
    """Get the path to the programs directory."""
    programs_path = os.path.join(get_app_data_path(), "programs")
    if not os.path.exists(programs_path):
        os.makedirs(programs_path, exist_ok=True)
    return programs_path