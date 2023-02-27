from datetime import datetime
import os
from PIL import ImageGrab
from pynput.keyboard import Listener, Key
import time

class Notes:

    def __init__(self, folder_path='') -> None:

        if folder_path == '':

            cur_dir = os.getcwd()
            self.folder_path = fr'{cur_dir}\cache\{str(datetime.now().strftime("%d-%m-%Y-%H-%M-%S"))}'
            print(f'Path was not specified, hence files are being cached at {self.folder_path}')

        else:
            self.folder_path = folder_path
        self.partial_path = self.folder_path.split("\\")[-1]

    def screenshot(self):
        im = ImageGrab.grab()

        if os.path.exists(self.folder_path):
            try: 
                cur = int([elem for elem in sorted(os.listdir(self.folder_path)) if elem.endswith('png')][-1].split('.')[0]) + 1
            except: cur = 1
        else:
            os.makedirs(self.folder_path)
            cur = 1

        im.save(fr'{self.folder_path}\{cur}.png')
        print(f'Stored {cur}.png at path ...\{self.partial_path}')

    def delete(self):
        if not os.path.exists(self.folder_path):
            print(f'Path does not exist.. Take a screenshot to initiate the path...')
            return False

        if len(os.listdir(self.folder_path)) == 0:
            print(f'Path does not have any file.. Take a screenshot to initiate the path...')
            return False
        
        file_list = os.listdir(self.folder_path)
        sorted_file_list = sorted(file_list, key=lambda x: os.path.getmtime(os.path.join(self.folder_path, x)))
        os.remove(os.path.join(self.folder_path, sorted_file_list[-1]))

        print(f'Removed {sorted_file_list[-1]} from path ...\{self.partial_path}')

    def on_press(self, key):
        if key == Key.f2:
            self.screenshot()

        elif key == Key.f4:
            self.delete()

        elif key == Key.f7:
            self.folder_path = input('Please enter the desired path: ')
            self.partial_path = self.folder_path.split("\\")[-1]

            print(f'Folder path successfully switched to {self.folder_path}...')


if __name__ == '__main__':

    with Listener(on_press=Notes().on_press) as lst:
        lst.join()