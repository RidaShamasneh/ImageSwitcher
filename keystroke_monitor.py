from pynput import keyboard
from pynput.keyboard import KeyCode

from PySide6.QtCore import QObject, Signal


class _KeyStrokeMonitorImplementation(QObject):
    """
    Actual implementation to monitor keystrokes
    """
    key_stroke_released = Signal(str)
    key_stroke_pressed = Signal(str)

    def __init__(self):
        super().__init__()
        self.__keyboard_listener = keyboard.Listener(on_press=self.__on_key_press, on_release=self.__on_key_release)

    def start(self) -> None:
        self.__keyboard_listener.start()
        self.__keyboard_listener.wait()

    def stop(self) -> None:
        self.__keyboard_listener.stop()

    def __on_key_press(self, key: KeyCode) -> None:
        if hasattr(key, 'char'):
            self.key_stroke_pressed.emit(key.char)

    def __on_key_release(self, key: KeyCode) -> None:
        if hasattr(key, 'char'):
            self.key_stroke_released.emit(key.char)


class KeyStrokeMonitor:
    """
    A singleton class to monitor keystrokes
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = _KeyStrokeMonitorImplementation()
        return cls.__instance
