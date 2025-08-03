from pathlib import Path
from typing import cast
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStyle,
    QStyleOption,
    QDialog,
    QPushButton,
    QPushButton,
    QButtonGroup,
    QDialogButtonBox,
)
from PySide6.QtGui import QGuiApplication, QPainter, QIcon
from PySide6.QtCore import Qt, QFile, QTextStream
from views.widgets import ListWidget
from .file_selector_dialog_item_widget import FileSelectorDialogItemWidget


class FileSelectorDialog(QDialog):
    """
    FileSelectorDialog is a dialog for selecting files with optional filtering.
    It allows users to select multiple files and apply filters to the displayed files.
    """

    def __init__(
        self,
        icon: str,
        files: list[Path],
        parent: QWidget = None,
        filters: bool = False,
        multiple: bool = False,
    ):
        super().__init__(parent)
        self.icon = icon
        self.files = files
        self.filters = filters
        self.multiple = multiple
        self.checked_files: list[Path] = []
        self.load_stylesheet(QGuiApplication.styleHints().colorScheme())
        self.setup_ui()
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.load_stylesheet)

    def setup_ui(self):
        self.setWindowTitle("Files Window")
        self.setWindowIcon(QIcon(":/assets/file.svg"))
        self.setMinimumSize(500, 300)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.main_layout)

        if self.filters:
            self.filter_widget = QWidget(self)
            self.filter_widget.setObjectName("FilterWidget")
            self.main_layout.addWidget(self.filter_widget)

            self.filter_layout = QHBoxLayout(self.filter_widget)
            self.filter_layout.setContentsMargins(0, 0, 0, 0)
            self.filter_layout.setSpacing(10)

            self.button_group = QButtonGroup(self)
            self.button_group.setExclusive(True)
            self.button_group.setObjectName("FilterButtons")

            self.parents = {f.parent for f in self.files}
            self.sorted_parents = sorted(self.parents, key=lambda p: str(p))

            for i in range(len(self.parents) + 1):
                button = QPushButton(self.filter_widget)
                button.setObjectName("FilterButton")
                button.setCheckable(True)
                button.setChecked(True if i == 0 else False)
                self.button_group.addButton(button)
                self.filter_layout.addWidget(button)

                if i == 0:
                    button.setText("All")
                    button.clicked.connect(lambda: self.set_filter("all"))
                    continue

                button.setText(self.sorted_parents[i - 1].name.capitalize())
                button.clicked.connect(
                    lambda _, p=self.sorted_parents[i - 1].name: self.set_filter(p)
                )

        self.file_list_widget = ListWidget(self)
        self.file_list_widget.setObjectName("FileListWidget")
        self.main_layout.addWidget(self.file_list_widget)

        self.file_group = QButtonGroup(self)
        self.file_group.setObjectName("FileGroup")
        self.file_group.setExclusive(
            False if self.multiple else True
        )  # Permite múltiples selecciones

        for file in self.files:
            item = FileSelectorDialogItemWidget(
                name=file.name,
                path=str(file),
                icon=self.icon,
                parent=self.file_list_widget,
            )
            item.toggled.connect(
                lambda checked, f=file: (
                    (
                        self.checked_files.append(f)
                        if checked
                        else self.checked_files.remove(f)
                    ),
                    print(f"Checked: {checked}"),
                    print(f"Checked files: {self.checked_files}"),
                )
            )
            self.file_list_widget.scroll_content_layout.addWidget(item)
            self.file_group.addButton(item)

        # ButtonBox estándar
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        button_box.accepted.connect(self.accept)  # manejar selección y luego accept()
        button_box.rejected.connect(self.reject)  # cierra con reject()
        self.main_layout.addWidget(button_box)

    def load_files(self, files: list[Path]):
        """
        Carga los archivos en el widget de lista.
        """
        for file in self.files:
            item = FileSelectorDialogItemWidget(
                name=file.name,
                path=str(file),
                icon=self.icon,
                parent=self.file_list_widget,
            )
            item.toggled.connect(
                lambda checked, f=file, cf=self.checked_files: (
                    (cf.append(f) if checked else cf.remove(f)),
                    print(f"Checked: {checked}"),
                    print(f"Checked files: {cf}"),
                )
            )
            self.file_list_widget.scroll_content_layout.addWidget(item)
            self.file_group.addButton(item)

    def set_filter(self, filter: str):
        """
        Aplica un filtro a los archivos mostrados en el widget de lista.
        """
        for i in range(self.file_list_widget.scroll_content_layout.count()):
            item = cast(
                FileSelectorDialogItemWidget,
                self.file_list_widget.scroll_content_layout.itemAt(i).widget(),
            )
            if item:
                item.setVisible(
                    filter.lower() in Path(item.path).parent.name.lower()
                    or filter == "all"
                )

    def load_stylesheet(self, scheme: Qt.ColorScheme):
        qss_file = QFile(
            f":/styles/{Path(__file__).stem}_{"dark" if scheme == Qt.ColorScheme.Dark else "light"}.qss"
        )
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(qss_file).readAll() + "\n"
            self.setStyleSheet(stylesheet)
            style = self.style()
            style.unpolish(self)
            style.polish(self)
            self.update()
            qss_file.close()

    def paintEvent(self, _):
        option = QStyleOption()
        option.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)
