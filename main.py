from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtGui import QPixmap
import sys

from krystroke_monitor import KeyStrokeMonitor


class ImageSwitcher(QWidget):
    WIDTH: int = 566
    HEIGHT: int = 900

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Key-Based Image Switcher")
        self.setFixedSize(ImageSwitcher.WIDTH, ImageSwitcher.HEIGHT)

        self.label = QLabel()
        self.label.setPixmap(QPixmap("image_0.png").scaled(ImageSwitcher.WIDTH, ImageSwitcher.HEIGHT))
        self.label.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.image_map = {
            "a": "image_0.png",
            "b": "image_1.png",
            "c": "image_2.png",
        }

        self.__keystroke_monitor = KeyStrokeMonitor()
        self.__keystroke_monitor.start()
        self.__keystroke_monitor.key_stroke_released.connect(self.__key_stroke_released_handler)

    def __key_stroke_released_handler(self, key: str) -> None:
        print(f"key -> {key}")
        image_path = self.image_map.get(key)
        if image_path:
            self.label.setPixmap(QPixmap(image_path).scaled(ImageSwitcher.WIDTH, ImageSwitcher.HEIGHT))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageSwitcher()
    window.show()
    sys.exit(app.exec())
