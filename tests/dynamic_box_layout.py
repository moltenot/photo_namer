"""Testing a layout where a QGrid is dynamically updated to have the appropriate number of columns for the width of
it's container
"""
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton
from PyQt6.QtCore import QSize, Qt


class MainWindow(QWidget):
    column_width = 150
    num_columns = 3

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Resizable Layout Example')
        self.setMinimumSize(QSize(self.num_columns * self.column_width, 200))

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.grid = QGridLayout()
        self.vbox.addLayout(self.grid)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.add_widgets()

    def remove_widgets(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def add_widgets(self):
        self.remove_widgets()
        for i in range(20):
            btn = QPushButton(f'Button {i}')
            self.grid.addWidget(btn, i // self.num_columns, i % self.num_columns)

    def resizeEvent(self, event):
        """this is automatically called on resize (it overrides the parent)"""
        # Update the number of columns based on the width of the window
        columns = event.size().width() // self.column_width
        if columns != self.num_columns:
            print(f"updating number of columns from {self.num_columns} to {columns}")

            self.num_columns = columns
            self.add_widgets()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
