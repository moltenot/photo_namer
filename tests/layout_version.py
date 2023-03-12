"""written by ChatGPT when asked to convert dynamic_box_layout to a QLayout"""
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QGridLayout, QWidget, QVBoxLayout, QPushButton


class ResizableGridLayout(QGridLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.column_width = 150
        self.num_columns = 3
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.add_widgets()

    def remove_widgets(self):
        while self.count():
            item = self.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def add_widgets(self):
        self.remove_widgets()
        for i in range(20):
            btn = QPushButton(f'Button {i}')
            self.addWidget(btn, i // self.num_columns, i % self.num_columns)

    def resizeEvent(self, event):
        columns = event.size().width() // self.column_width
        if columns != self.num_columns:
            self.num_columns = columns
            self.add_widgets()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Resizable Layout Example')
        self.setMinimumSize(QSize(450, 200))

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.grid = ResizableGridLayout()
        self.vbox.addLayout(self.grid)


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
