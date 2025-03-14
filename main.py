import sys
from PySide6.QtWidgets import QApplication
from views.home_window.home_window import HomeWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec())
