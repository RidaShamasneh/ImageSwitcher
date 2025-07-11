import sys
import os

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtGui import QMovie

from keystroke_monitor import KeyStrokeMonitor


class ImageSwitcher(QWidget):
    WIDTH: int = 400
    HEIGHT: int = 800

    INITIAL_IMAGE_KEY: str = "initial"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mobile")

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.__label = QLabel()
        self.__movie = None

        layout = QVBoxLayout()
        layout.addWidget(self.__label)
        self.setLayout(layout)

        root_dir = os.path.dirname(os.path.realpath(__file__))
        # root_dir is e.g. 'C:\Users\Admin\PycharmProjects\ImageSwitcher'
        resources_path = os.path.join(root_dir, "resources")
        print(f"Info: resources_path = {resources_path}")

        self.__image_map: dict[str, str] = {
            ImageSwitcher.INITIAL_IMAGE_KEY: os.path.join(resources_path, "initial.gif")
        }

        for dirpath, dirnames, filenames in os.walk(resources_path):
            for sub_dirname in dirnames:
                image_path: str = os.path.join(dirpath, sub_dirname, "image.gif")
                self.__image_map[sub_dirname.lower()] = image_path
                print(self.__image_map[sub_dirname])

        self.__keystroke_monitor = KeyStrokeMonitor()
        self.__keystroke_monitor.start()
        self.__keystroke_monitor.key_stroke_released.connect(self.__key_stroke_released_handler)

        self.__label.setStyleSheet("background-color: black;")

        # Set initial image on startup
        self.__key_stroke_released_handler(ImageSwitcher.INITIAL_IMAGE_KEY)

    def __key_stroke_released_handler(self, key: str) -> None:
        key = key.lower()

        print(f"Info: key pressed -> {key}")
        if key not in self.__image_map:
            print("Warning: No entry for this key.")
            return

        image_path: str = self.__image_map.get(key)
        if not image_path:
            print("Error: No image associated with this key!")
            return

        if not os.path.isfile(image_path):
            print(f"Error: \"{image_path}\" was not found!")
            return

        if self.__movie and self.__movie.state() == QMovie.Running:
            self.__movie.stop()

        self.__movie = QMovie(image_path)
        self.__movie.setScaledSize(QSize(ImageSwitcher.WIDTH, ImageSwitcher.HEIGHT))
        self.__label.setMovie(self.__movie)

        self.__movie.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageSwitcher()
    window.show()
    sys.exit(app.exec())
