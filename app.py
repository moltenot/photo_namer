import sys
import os

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QFileDialog, QPushButton, QMainWindow


class PhotoNamer(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Photo Namer")

        self.setCentralWidget(PickADir(self))


class PickADir(QWidget):
    files: list[str]
    dir: str

    def __init__(self, parent):
        super().__init__(parent)
        print("I am a pick a dir widget")

        button = QPushButton("Select a Photo Album", parent=self)
        button.clicked.connect(self.set_dir)
        # self.setCentralWidget(button)

    def set_dir(self):
        self.dir = str(QFileDialog.getExistingDirectory(
            self, "Select a Directory"))
        print(f"user selected {self.dir}")
        self.files = os.scandir(self.dir)
        print("this directory contains")
        for f in self.files:
            print(f)


if __name__ == "__main__":
    app = QApplication([])
    window = PhotoNamer()
    window.show()
    sys.exit(app.exec())
