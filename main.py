import sys
import assets.assets_rc
import styles.styles_rc
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QGuiApplication, Qt

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QGuiApplication.styleHints().setColorScheme(Qt.ColorScheme.Dark)

    current_workspace = str(settings.value("current_workspace", ""))
    print(Path(__file__).name, f"Current workspace value: {current_workspace}")

    current_worksapce = Path(current_workspace) if current_workspace != "" else ""
    print(Path(__file__).name, f"Current workspace: {current_workspace == ''}")

    if current_workspace == '' or not current_worksapce.exists():

        from views import HomeWindow
        from controllers import HomeWindowController

        home_window = HomeWindow()
        home_window_controller = HomeWindowController(home_window)

        home_window.show()
        center_window_on_screen(home_window)

    elif current_worksapce.exists():

        from views import MainWindow
        from controllers import MainWindowController

        main_window = MainWindow()
        main_window_controller = MainWindowController(main_window)

        main_window.show()
        center_window_on_screen(main_window)

    sys.exit(app.exec())
