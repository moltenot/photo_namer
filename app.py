from PyQt6.QtWidgets import QInputDialog, QLineEdit
import sys
import os
from os.path import join

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QFileDialog, QPushButton, QMainWindow, QHBoxLayout, QVBoxLayout, QScrollArea, QInputDialog, QDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtCore import pyqtSignal
aspect_ratio_mode = Qt.AspectRatioMode.KeepAspectRatio


class PhotoNamer(QMainWindow):
    album_path: str

    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Photo Namer")

        everything_widget = QWidget(self)

        self.file_list = FileList(self)

        layout = QVBoxLayout()
        layout.addWidget(PickADir(self, self.set_album_path))
        layout.addWidget(self.file_list)

        everything_widget.setLayout(layout)

        self.setCentralWidget(everything_widget)

    def set_album_path(self, path):
        print("setting album path to", path)
        self.album_path = path
        self.file_list.update(path)


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
            print(self.exec_())
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

    def showInputDialog(self):
        text, ok = CustomInputDialog(self).getText("Enter the title of the image")

        if ok:
            print(f'set filename to, {text}!')
            self.label_label.setText(
                f"{self.number_in_dir:02d}_{text.replace(' ', '_')}.{self.suffix}")

    def mousePressEvent(self, event):
        # get input from the user
        self.showInputDialog()

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
        max_size = 300
        if pixmap.width() > max_size or pixmap.height() > max_size:
            pixmap = pixmap.scaled(
                max_size, max_size, aspectRatioMode=aspect_ratio_mode, transformMode=Qt.TransformationMode.SmoothTransformation)

        if pixmap.isNull():
            raise Exception("not an image")

        self.image_label.setPixmap(pixmap)

        self.setLayout(self.layout)


class FileList(QWidget):

    file_list: list[str]
    album_path: str

    def __init__(self, parent):
        super().__init__(parent)

        self.file_list = ["file 1", "file 2"]

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Scroll Area which contains the widgets, set as the centralWidget
        self.scroll = QScrollArea()
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.vbox = QVBoxLayout()

        for i in range(1, 50):
            object = QLabel("TextLabel")
            self.vbox.addWidget(object)

        self.widget.setLayout(self.vbox)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.layout.addWidget(self.scroll)
        self.album_path = None

        ##########
        # todo delete
        self.album_path = "/home/theo/Projects/photo_namer_tool/test_album"
        self.update(self.album_path)
        ##########

        self._update_labels()

    def _update_labels(self):
        """update the labels on this widget from the self.file_list attribute """
        self._clear_labels()
        count = 1
        for f in self.file_list:
            if self.album_path:
                image_path = join(self.album_path, f)
                try:
                    image_label = EditableImage(image_path, count)
                    count += 1
                except Exception:
                    continue

            self.vbox.addWidget(image_label)

    def _clear_labels(self):
        while self.vbox.count():
            child = self.vbox.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update(self, album_path):
        print("updating file list to look at ", album_path)
        self.album_path = album_path
        self.file_list = os.listdir(album_path)
        self._update_labels()


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


if __name__ == "__main__":
    app = QApplication([])
    window = PhotoNamer()
    window.show()
    sys.exit(app.exec())
