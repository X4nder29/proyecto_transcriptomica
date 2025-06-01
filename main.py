import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from utils import center_window_on_screen, settings

if __name__ == "__main__":
    app = QApplication(sys.argv)

    current_worksapce = Path(settings.value("current_workspace", ""))
    print(Path(__file__).name, f'Current workspace: {current_worksapce}')

    if current_worksapce.exists():
        from views import MainWindow
        from controllers import MainWindowController

        main_window = MainWindow()
        main_window_controller = MainWindowController(main_window)

        main_window.show()
        center_window_on_screen(main_window)
    else:
        from views import HomeWindow
        from controllers import HomeWindowController

        home_window = HomeWindow()
        home_window_controller = HomeWindowController(home_window)

        home_window.show()
        center_window_on_screen(home_window)

    sys.exit(app.exec())
