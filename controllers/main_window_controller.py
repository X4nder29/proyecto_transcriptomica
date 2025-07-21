from pathlib import Path
from functools import partial
from utils import (
    center_window_on_screen,
    get_current_workspace,
    clear_current_workspace,
)
from views import MainWindow


class MainWindowController:

    def __init__(self, view: MainWindow):
        self.view = view

        self.check_existing_workspace()

        self.view.side_bar.close_workspace.triggered.connect(
            partial(self.close_workspace_action)
        )

        self.view.side_bar.home_button.toggled.connect(self._on_home)
        self.view.side_bar.kraken_button.toggled.connect(self._on_kraken)
        self.view.side_bar.settings_button.toggled.connect(self._on_settings)

    def check_existing_workspace(self):
        # Check if the current workspace exists
        current_workspace = get_current_workspace()

        if current_workspace is None or not current_workspace.exists():
            from views import HomeWindow
            from controllers import HomeWindowController

            home_window = HomeWindow()
            HomeWindowController(home_window)

            self.view.close()

            home_window.show()
            center_window_on_screen(home_window)

    def close_workspace_action(self):
        """
        Close the current workspace and return to the home window.
        """
        clear_current_workspace()

        from views import HomeWindow
        from controllers import HomeWindowController

        home_window = HomeWindow()
        HomeWindowController(home_window)

        self.view.close()

        home_window.show()
        center_window_on_screen(home_window)

        print(
            Path(__file__).name,
            "-",
            "Closed current workspace and returned to home window.",
        )

    def _on_home(self, checked: bool):
        if checked:
            self.view.content.home_panel_controller.load_workspace_files()

    def _on_fastqc(self):
        pass

    def _on_trimmomatic(self):
        pass

    def _on_sortmerna(self):
        pass

    def _on_kraken(self, checked: bool):
        if checked:
            self.view.content.kraken2_controller._load_existing_report()

    def _on_settings(self, checked: bool):
        if checked:
            self.view.content.settings_panel_controller.check_installed()
