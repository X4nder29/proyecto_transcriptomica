import sys
import assets.assets_rc
import styles.styles_rc
import views.support_window.content.manual_rc
from pathlib import Path
from PySide6.QtWidgets import QApplication
from utils import set_default_settings, center_window_on_screen, get_current_workspace
from app_state import AppState

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.state = AppState

    set_default_settings()

    current_workspace = get_current_workspace()
    print(Path(__file__).name, f"Current workspace value: {current_workspace}")

    if current_workspace is None or not current_workspace.exists():

        from views import HomeWindow
        from controllers import HomeWindowController

        home_window = HomeWindow()
        home_window_controller = HomeWindowController(home_window)

        home_window.show()
        center_window_on_screen(home_window)

    elif current_workspace.exists():

        from views import MainWindow
        from controllers import MainWindowController

        main_window = MainWindow()
        main_window_controller = MainWindowController(main_window)

        main_window.show()
        center_window_on_screen(main_window)

    sys.exit(app.exec())
