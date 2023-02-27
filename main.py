from pynput.keyboard import Listener, Key
import time

class Notes:

    def __init__(self, folder_path='') -> None:
        self.folder_path = folder_path

    def on_press(self, key):
        if key == Key.f2 and key not in self.keys:
            print('Take Screenshot')

        elif key == Key.f4:
            print('Screenshot Deleted')

        elif key == Key.f7:
            print('Folder Path')


if __name__ == '__main__':

    with Listener(on_press=Notes().on_press) as lst:
        lst.join()