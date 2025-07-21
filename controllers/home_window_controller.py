import shutil
from pathlib import Path
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from views import HomeWindow, CreateWorkspaceDialog
from utils import (
    center_window_on_screen,
    set_current_workspace,
    get_workspaces,
    add_new_workspace,
    remove_workspace,
)
from views.home_window.widgets import WorkspaceItem


class HomeWindowController:

    def __init__(self, view: HomeWindow):
        self.view = view
        self.view.body.empty_workspace.create_button.clicked.connect(
            self.create_new_workspace
        )
        self.view.body.empty_workspace.open_button.clicked.connect(
            self.load_existing_workspace
        )
        self.view.body.workspaces.create_new_workspace_button.clicked.connect(
            self.create_new_workspace
        )
        self.view.body.workspaces.open_existing_workspace_button.clicked.connect(
            self.load_existing_workspace
        )
        self.view.body.workspaces.search_line_edit.textChanged.connect(
            self.search_workspace
        )

        self.has_workspaces()

    def create_new_workspace(self):
        self.create_workspace_dialog = CreateWorkspaceDialog(self.view)
        self.create_workspace_dialog.location_button.clicked.connect(
            self.open_file_dialog
        )
        result = self.create_workspace_dialog.exec_()

        if result == QDialog.Accepted:
            name = self.create_workspace_dialog.name_input.text()
            location = Path(self.create_workspace_dialog.location_input.text())

            workspace_path = location / name
            if not workspace_path.exists():
                workspace_path.mkdir(parents=True, exist_ok=True)

            workspace_file_path = workspace_path / "project.json"

            if not workspace_file_path.exists():
                workspace_file_path.write_text("{}")

            source_folder_path = workspace_path / "source"
            if not source_folder_path.exists():
                source_folder_path.mkdir(parents=True, exist_ok=True)

            reports_folder_path = workspace_path / "reports"
            if not reports_folder_path.exists():
                reports_folder_path.mkdir(parents=True, exist_ok=True)

            trimmed_folder_path = workspace_path / "trimmed"
            if not trimmed_folder_path.exists():
                trimmed_folder_path.mkdir(parents=True, exist_ok=True)

            sorted_folder_path = workspace_path / "sorted"
            if not sorted_folder_path.exists():
                sorted_folder_path.mkdir(parents=True, exist_ok=True)

            krakened_folder_path = workspace_path / "krakened"
            if not krakened_folder_path.exists():
                krakened_folder_path.mkdir(parents=True, exist_ok=True)

            # Add the new workspace to the settings
            add_new_workspace(workspace_path)

            self.has_workspaces()

    def load_existing_workspace(self):
        workspace_path = QFileDialog.getExistingDirectory(
            self.view,
            "Seleccionar espacio de trabajo",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )

        if not workspace_path:
            print("No se seleccionó ningún espacio de trabajo")
            QMessageBox.warning(
                self.view, "Error", "No se seleccionó ningún espacio de trabajo"
            )
            return

        workspace_path = Path(workspace_path)
        required_files = [
            Path("project.json"),
        ]
        required_folders = [
            Path("reports"),
            Path("trimmed"),
            Path("sorted"),
            Path("krakened"),
            Path("source"),
        ]

        if not all((workspace_path / file).exists() for file in required_files):
            QMessageBox.warning(
                self.view,
                "Error",
                "El espacio de trabajo seleccionado no es valido.",
            )
            return

        if not all((workspace_path / folder).exists() for folder in required_folders):
            QMessageBox.warning(
                self.view,
                "Error",
                "El espacio de trabajo seleccionado no es valido.",
            )
            return

        add_new_workspace(workspace_path)
        self.has_workspaces()

    def open_file_dialog(self):
        directory_path = QFileDialog.getExistingDirectory(
            self.view,
            "Seleccionar directorio",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )

        if directory_path:
            print(f"Directorio seleccionado: {directory_path}")
            self.create_workspace_dialog.location_input.setText(directory_path)
        else:
            print("No se seleccionó ningún directorio")
            QMessageBox.warning(
                self.view, "Error", "No se seleccionó ningún directorio"
            )

    def has_workspaces(self):
        workspaces = get_workspaces()

        if not workspaces:
            self.view.body.main_layout.setCurrentWidget(self.view.body.empty_workspace)
        else:
            self.view.body.main_layout.setCurrentWidget(self.view.body.workspaces)
            self.load_workspace_item(workspaces)

    def load_workspace_item(self, workspaces):

        for i in range(self.view.body.workspaces.workspaces_list_layout.count()):
            item = self.view.body.workspaces.workspaces_list_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        for workspace in workspaces:

            workspace_path = Path(workspace)

            workspace_item = WorkspaceItem(
                workspace_path.stem,
                workspace_path,
                self.view.body.workspaces.workspaces_list,
            )
            workspace_item.clicked.connect(
                lambda path=workspace_path: self.open_workspace(path)
            )
            workspace_item.delete_action.triggered.connect(
                lambda _, item=workspace_item: self.delete_workspace(item)
            )
            self.view.body.workspaces.workspaces_list_layout.addWidget(workspace_item)

    def open_workspace(self, workspace_path: Path):
        set_current_workspace(workspace_path)

        self.view.close()

        from views import MainWindow
        from controllers import MainWindowController

        main_window = MainWindow()
        MainWindowController(main_window)

        main_window.show()
        center_window_on_screen(main_window)

    def delete_workspace(self, workspace_item: WorkspaceItem):
        reply = QMessageBox.question(
            self.view,
            "Confirmar eliminación",
            f"¿Estás seguro de que quieres eliminar el espacio de trabajo '{workspace_item.name}'?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            remove_workspace(workspace_item.path)

            workspace_path = workspace_item.path
            if workspace_path.exists() and workspace_path.is_dir():
                shutil.rmtree(workspace_item.path)

            workspace_item.deleteLater()
            self.has_workspaces()

    def search_workspace(self, search_text: str):
        for i in range(self.view.body.workspaces.workspaces_list_layout.count()):
            item = self.view.body.workspaces.workspaces_list_layout.itemAt(i)
            if item.widget():
                workspace_item = item.widget()
                if search_text.lower() in workspace_item.name.lower():
                    workspace_item.show()
                else:
                    workspace_item.hide()
