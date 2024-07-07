from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QLineEdit, QListWidget, QLabel, QGridLayout


class CentralWidget(QWidget):

    ProgramNameChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.fixtures = QListWidget()

        self.program_name = QLineEdit()
        self.program_name.setMaxLength(7)
        self.program_name.textChanged.connect(self.ProgramNameChanged)

        layout = QGridLayout(self)
        layout.addWidget(QLabel("Current program name"), 0, 0)
        layout.addWidget(self.program_name, 1, 0)
        layout.addWidget(QWidget(), 2, 0)

        layout.addWidget(self.fixtures, 0, 1, 3, 1)

        layout.setRowStretch(2, 100)

    def set_program_name(self, name: str):
        self.program_name.setText(name)

    def get_program_name(self) -> str:
        return self.program_name.text()

    def set_fixture_names(self, names: list[str]):
        current_names = [self.fixtures.item(i).text() for i in range(self.fixtures.count())]
        if current_names == names:
            return

        self.fixtures.clear()
        self.fixtures.addItems(names)

    def set_selected_fixture(self, index: int):
        current_selected_fixture_index = self.fixtures.currentRow()
        if current_selected_fixture_index == index:
            return

        self.fixtures.setCurrentRow(index)
