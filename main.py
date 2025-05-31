import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QCursor
from views import HomeWindow
from controllers import HomeWindowController
from utils import center_window_on_screen

if __name__ == "__main__":
    app = QApplication(sys.argv)

    screen = app.screenAt(QCursor.pos())
    center_point = screen.availableGeometry().center()

    home_window = HomeWindow()
    home_window_controller = HomeWindowController(home_window)
    center_window_on_screen(home_window)

    home_window.show()

    sys.exit(app.exec())
