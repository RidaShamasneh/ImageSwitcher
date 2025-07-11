import sys

from pynput import keyboard
from pynput.keyboard import KeyCode

from PySide6.QtCore import QObject, Signal


class _KeyStrokeMonitorImplementation(QObject):
    """
    Actual implementation to monitor long button press for 1 second
    """
    key_stroke_released = Signal(str)
    key_stroke_pressed = Signal(str)

    def __init__(self):
        super().__init__()

        self.__keyboard_listener = keyboard.Listener(on_press=self.__on_key_press, on_release=self.__on_key_release)

        self.__fix_caps_lock_crash_on_macos()

    def __fix_caps_lock_crash_on_macos(self):
        """
        This function provides a workaround to prevent a crash on macOS when pressing the Caps Lock key.
        The solution involves removing Quartz.CGEventMaskBit(Quartz.NSSystemDefined) from the key events we listen to by overriding
        _darwin.Listener._EVENTS. By selectively setting the event mask, we avoid issues with system-defined keys while retaining
        the ability to listen for other key events. Please note that commenting out this line results in the inability to listen
        to system-defined keys, which is not a concern in our use case, as we only need to listen to the 'q' and 'Q' keys.
        """
        if sys.platform == 'darwin':
            import Quartz
            darwin_events = (
                    Quartz.CGEventMaskBit(Quartz.kCGEventKeyDown) |
                    Quartz.CGEventMaskBit(Quartz.kCGEventKeyUp) |
                    Quartz.CGEventMaskBit(Quartz.kCGEventFlagsChanged)
            )
            keyboard._darwin.Listener._EVENTS = darwin_events

    def __is_quit_key(self, key: KeyCode):
        return key == KeyCode.from_char('q') or key == KeyCode.from_char('Q')

    def start(self) -> None:
        self.__keyboard_listener.start()
        self.__keyboard_listener.wait()

    def stop(self) -> None:
        self.__keyboard_listener.stop()

    def __on_key_press(self, key) -> None:
        self.key_stroke_pressed.emit(key.char)

    def __on_key_release(self, key: KeyCode) -> None:
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
