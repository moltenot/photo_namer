import sys
import os

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QFileDialog, QPushButton, QMainWindow, QHBoxLayout, QVBoxLayout


class PhotoNamer(QMainWindow):
    album_path: str

    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Photo Namer")

        everything_widget = QWidget(self)

        self.file_list = FileList(self)

        layout = QHBoxLayout()
        layout.addWidget(PickADir(self, self.set_album_path))
        layout.addWidget(self.file_list)

        everything_widget.setLayout(layout)

        self.setCentralWidget(everything_widget)
        

    def set_album_path(self, path):
        print("setting album path to", path)
        self.album_path = path
        self.file_list.update(path)


class FileList(QWidget):

    file_list: list[str]

    def __init__(self, parent):
        super().__init__(parent)

        self.file_list = ["file 1", "file 2"]
        layout = QVBoxLayout()
        self.setLayout(layout)

        self._update_labels()

    def _update_labels(self):
        """update the labels on this widget from the self.file_list attribute """
        self._clear_labels()
        for f in self.file_list:
            label = QLabel(self)
            label.setText(f)
            self.layout().addWidget(label)

    def _clear_labels(self):
        while self.layout().count():
            child = self.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update(self, album_path):
        print("updating file list to look at ", album_path)
        self.file_list = os.listdir(album_path)
        self._update_labels()


class PickADir(QWidget):
    files: list[str]
    dir: str

    def __init__(self, parent, on_pick_album_callback):
        super().__init__(parent)
        self.on_pick_album_callback = on_pick_album_callback

        button = QPushButton("Select a Photo Album", parent=self)
        self.setFixedWidth(250)
        button.clicked.connect(self.set_dir)


    def set_dir(self):
        self.dir = str(QFileDialog.getExistingDirectory(
            self, "Select a Directory"))
        self.on_pick_album_callback(self.dir)


if __name__ == "__main__":
    app = QApplication([])
    window = PhotoNamer()
    window.show()
    sys.exit(app.exec())
