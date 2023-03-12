"""written by ChatGPT when asked to convert dynamic_box_layout to a QLayout"""
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QLayout, QWidget, QPushButton, QVBoxLayout, QGridLayout


class ResizableGridLayout(QLayout):
    column_width = 150
    num_columns = 3

    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid = QGridLayout()
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.addLayout(self.grid)

        self.widgets = []

    def addItem(self, item):
        pass

    def addWidget(self, widget):
        self.widgets.append(widget)
        self.updateWidgets()

    def count(self):
        return len(self.widgets)

    def itemAt(self, index):
        if index < 0 or index >= len(self.widgets):
            return None
        return self.widgets[index]

    def takeAt(self, index):
        if index < 0 or index >= len(self.widgets):
            return None
        return self.widgets.pop(index)

    def sizeHint(self):
        return QSize(self.num_columns * self.column_width, 200)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.updateWidgets()

    def updateWidgets(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        for i, widget in enumerate(self.widgets):
            row = i // self.num_columns
            col = i % self.num_columns
            self.grid.addWidget(widget, row, col)

    def updateNumColumns(self):
        width = self.geometry().width()
        columns = width // self.column_width
        if columns != self.num_columns:
            self.num_columns = columns
            self.updateWidgets()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Resizable Layout Example')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.grid_layout = ResizableGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.add_widgets()

    def add_widgets(self):
        for i in range(20):
            btn = QPushButton(f'Button {i}')
            self.grid_layout.addWidget(btn)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.grid_layout.updateNumColumns()


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
