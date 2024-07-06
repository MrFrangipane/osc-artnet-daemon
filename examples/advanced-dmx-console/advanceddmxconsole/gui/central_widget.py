from PySide6.QtWidgets import QWidget, QLineEdit, QListWidget, QLabel, QGridLayout

from advanceddmxconsole.advanced_dmx_console import AdvancedDmxConsole


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.fixtures = QListWidget()

        self.program_name = QLineEdit()
        self.program_name.setMaxLength(7)

        layout = QGridLayout(self)
        layout.addWidget(QLabel("Current program name"), 0, 0)
        layout.addWidget(self.program_name, 1, 0)
        layout.addWidget(QWidget(), 2, 0)

        layout.addWidget(self.fixtures, 0, 1, 3, 1)

        layout.setRowStretch(2, 100)

    def a(self):
        for fixture in AdvancedDmxConsole().fixture_repository.fixtures:
            self.fixtures.addItem(fixture.info.name)
