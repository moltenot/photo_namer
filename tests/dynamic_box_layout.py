from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QSize


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Resizable Layout Example')
        self.setMinimumSize(QSize(300, 200))

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.grid = QGridLayout()
        self.vbox.addLayout(self.grid)

        for i in range(20):
            btn = QPushButton(f'Button {i}')
            self.grid.addWidget(btn, i // 4, i % 4)


    def resizeEvent(self, event):
        # Update the number of columns based on the width of the window
        print("resize event",event)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
