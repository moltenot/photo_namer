import os
import shutil
import sys
from os.path import join

from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QFileDialog, QPushButton, QMainWindow, QHBoxLayout, \
    QVBoxLayout, QScrollArea, QDialog
from PyQt6.QtWidgets import QLineEdit, QGridLayout

aspect_ratio_mode = Qt.AspectRatioMode.KeepAspectRatio

IMAGE_WIDTH = 200


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()


class CustomInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # create a custom line edit
        self.lineEdit = CustomLineEdit()

        # create buttons
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        # create a layout for the buttons
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)

        # create a layout for the label and line edit
        inputLayout = QVBoxLayout()
        inputLayout.addWidget(QLabel("Enter text:"))
        inputLayout.addWidget(self.lineEdit)
        inputLayout.addLayout(buttonLayout)

        self.setLayout(inputLayout)

        # set up connections
        okButton.clicked.connect(self.accept)
        cancelButton.clicked.connect(self.reject)

    def getText(self, label):
        self.setWindowTitle(label)
        if self.exec() == QDialog.DialogCode.Accepted:
            print("accepted")
            return self.lineEdit.text(), True
        else:
            print("not accepted")
            return None, False


class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.textChanged.connect(self.modifyText)

    def modifyText(self, text):
        text = text.replace(' ', '_')
        self.setText(text)


class EditableImage(QWidget):
    old_filename: str
    new_filename = None  # set to string when you know it
    num_digits: int  # the number of digits needed to identify this image in the folder

    def showInputDialog(self):
        print("showing input dialog")
        text, ok = CustomInputDialog(self).getText(
            "Enter the title of the image")

        print(f"get text closed, received {text} {ok}")

        if ok:
            self.new_filename = f"{self.number_in_dir:0{self.num_digits}d}_{text.replace(' ', '_')}.{self.suffix}"
            print(f'new filename: {self.new_filename}')
            self.label_label.setText(self.new_filename)

    def mousePressEvent(self, event):
        # get input from the user
        self.showInputDialog()

    def set_num_digits(self, num_digits):
        """set the number of digits needed to represent this file. i.e. 3 digits if there are 100+ images in the directory"""
        self.num_digits = num_digits

    def __init__(self, image_path, number_in_dir):
        super().__init__()

        self.image_path = image_path
        self.filename = os.path.basename(image_path)
        self.number_in_dir = number_in_dir
        self.old_filename = os.path.basename(image_path)
        self.suffix = self.old_filename.split(".")[-1]
        self.layout = QVBoxLayout()

        self.image_label = QLabel(self.image_path)
        self.label_label = QLabel(self.filename)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.label_label)

        pixmap = QPixmap(self.image_path)
        # scale pixmap if it is too large
        max_size = IMAGE_WIDTH
        if pixmap.width() > max_size or pixmap.height() > max_size:
            pixmap = pixmap.scaled(
                max_size, max_size, aspectRatioMode=aspect_ratio_mode,
                transformMode=Qt.TransformationMode.SmoothTransformation)

        if pixmap.isNull():
            raise Exception("not an image")

        self.image_label.setPixmap(pixmap)

        self.setLayout(self.layout)


class PickADir(QWidget):
    files: list[str]
    dir: str

    def __init__(self, parent, on_pick_album_callback):
        super().__init__(parent)
        self.on_pick_album_callback = on_pick_album_callback
        self.layout = QVBoxLayout()
        button = QPushButton("Select a Photo Album")
        button.clicked.connect(self.set_dir)

        self.layout.addWidget(button)
        self.setLayout(self.layout)

    def set_dir(self):
        self.dir = str(QFileDialog.getExistingDirectory(
            self, "Select a Directory"))
        self.on_pick_album_callback(self.dir)


class FileList(QWidget):
    column_width = IMAGE_WIDTH
    num_columns = 3
    file_list = []  # file names
    editable_images = []  # editable image widgets
    album_path: str

    def __init__(self, parent):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Scroll Area which contains the widgets, set as the centralWidget
        self.scroll = QScrollArea()
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.grid = QGridLayout()

        self.widget.setLayout(self.grid)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.layout.addWidget(self.scroll)
        self.album_path = None

        self.parent().setMinimumSize(600, 600)
        self.pick_a_dir = PickADir(self, self.update_album_path)
        self.layout.addWidget(self.pick_a_dir)

    def write_filename_changes(self):
        print("write filename changes")
        print(self.album_path)
        for ei in self.editable_images:
            print(ei.old_filename)
            if ei.new_filename:
                print(f"has a new filename of {ei.new_filename}")
                # shutil.move(join(self.album_path, ei.old_filename), join(self.album_path, ei.new_filename))
            else:
                print("doesn't have a new filename")

        # set the UI back
        self.write_button.deleteLater()
        self.pick_a_dir = PickADir(self, self.update_album_path)
        self.layout.addWidget(self.pick_a_dir)
        self.remove_widgets()
        self.file_list = []

    def _cache_images(self):
        """takes the images in the given directory, and create EditableImage widgets from them"""
        print(f"caching images in {self.album_path}")

        if not self.album_path:
            return

        count = 1
        for f in self.file_list:
            image_path = join(self.album_path, f)
            try:
                image_label = EditableImage(image_path, count)
                count += 1
                self.editable_images.append(image_label)
                print(f"cached {f}")
            except Exception:
                continue

        num_images = len(self.editable_images)
        self.num_digits = len(str(num_images))
        for ei in self.editable_images:
            ei.set_num_digits(self.num_digits)
        print(f"cached {num_images} images, which is {self.num_digits} digits")

    def _update_labels(self):
        """update the labels on this widget from the self.file_list attribute """
        for i, ei in enumerate(self.editable_images):
            print("number of columns", self.num_columns)
            self.grid.addWidget(ei, i // self.num_columns, i % self.num_columns)

    def _clear_labels(self):
        """clear the labels from the grid layout, so they can be added again (potentially in a new configuration)"""
        for ei in self.editable_images:
            self.grid.removeWidget(ei)

    def remove_widgets(self):
        """remove all traces of editable images, so you can look at a new folder as a photo album"""
        self.editable_images = []
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def update_album_path(self, album_path):
        print("updating file list to look at ", album_path)
        self.album_path = album_path
        self.remove_widgets()
        self.file_list = os.listdir(album_path)
        self._clear_labels()
        self._cache_images()
        self._update_labels()
        self.num_columns = 3

        # change the bottom buttons from the "pick a dir" button to the write changes button
        # self.layout.removeWidget(self.pick_a_dir)
        self.pick_a_dir.deleteLater()
        self.write_button = QPushButton("Write new filenames")
        self.write_button.clicked.connect(self.write_filename_changes)
        self.layout.addWidget(self.write_button)

    def resizeEvent(self, event):
        """this is automatically called on resize (it overrides the parent)"""
        # Update the number of columns based on the width of the window
        min_columns = 1
        columns = max(event.size().width() // self.column_width, min_columns)
        if columns != self.num_columns:
            print(f"updating number of columns from {self.num_columns} to {columns}")
            self.num_columns = columns
            self._update_labels()


class PhotoNamer(QMainWindow):
    album_path: str

    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Photo Namer")

        everything_widget = QWidget(self)

        self.file_list = FileList(self)

        layout = QVBoxLayout()
        layout.addWidget(self.file_list)
        everything_widget.setLayout(layout)

        self.setCentralWidget(everything_widget)

    def set_album_path(self, path):
        print("setting album path to", path)
        self.album_path = path
        self.file_list.update_album_path(path)


if __name__ == "__main__":
    app = QApplication([])
    window = PhotoNamer()
    window.show()
    sys.exit(app.exec())
