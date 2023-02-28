import argparse
from datetime import datetime
import json
import keyboard
import os
from PIL import ImageGrab
from pynput.keyboard import Listener, Key
import re

class Notes:

    def __init__(self, folder_path='') -> None:

        parser = argparse.ArgumentParser()
        parser.add_argument("--path", default=False)
        parser.add_argument("--default-path", default=False)
        parser.add_argument("--audio-on", default=False, action="store_true")
        parser.add_argument("--last-path", default=False, action="store_true")
        parser.add_argument("--path-offset", default=False)
        self.args = parser.parse_args()

        if self.args.default_path:
            self.store('Path', self.args.default_path)

        if self.args.path_offset:
            temp_path = json.load(open('data.json', 'r'))['Path']
            self.folder_path = f'{temp_path}\\{self.args.path_offset}'

        elif folder_path == '':

            if self.args.path:
                self.folder_path = self.args.path

            elif self.args.last_path:
                with open('data.json', 'r') as fp:
                    self.folder_path = json.load(fp)['Last_Path']

            elif os.path.exists('data.json'):
                with open('data.json', 'r') as fp:
                    self.folder_path = json.load(fp)['Path']
            
            else:
                cur_dir = os.getcwd()
                self.folder_path = fr'{cur_dir}\cache\{str(datetime.now().strftime("%d-%m-%Y-%H-%M-%S"))}'
                print(Notes.colored(f'Path was not specified, hence files are being cached at {self.folder_path}', 'red'))

        else:
            self.folder_path = folder_path
        self.store('Last_Path', self.folder_path)
        self.partial_path = self.set_partial_path()

        print(Notes.colored(f'Current Path: {self.folder_path}', 'blue'))

    def set_partial_path(self):

        try:
            temp_path = json.load(open('data.json', 'r'))['Path']
            if temp_path.split('\\')[-1] in self.folder_path:
                return self.folder_path.split(temp_path.split('\\')[-1])[-1]
        except:
            pass
        
        if os.getcwd().split('\\')[-1] in self.folder_path:
            return self.folder_path.split(os.getcwd().split('\\')[-1])[-1]
        else:
            return self.folder_path.split("\\")[-1]

    def store(self, key, value):
        
        value = value.replace('/', '\\')
        value = fr'{value}'

        if os.path.exists('data.json'):
            with open('data.json', 'r') as fp:
                cont = json.load(fp)
                cont[key] = value
        else: cont = {key: value}

        with open('data.json', 'w') as fp:
            json.dump(cont, fp)

    def screenshot(self):
        im = ImageGrab.grab()

        if os.path.exists(self.folder_path):

            try: 
                filenames = [f for f in os.listdir(self.folder_path) if re.match(r"\d+\.png", f)]
                cur = max([int(re.search(r"\d+", f).group()) for f in filenames]) + 1

            except: cur = 1

        else:
            os.makedirs(self.folder_path)
            cur = 1

        im.save(fr'{self.folder_path}\{cur}.png')
        print(Notes.colored(f'Stored {cur}.png at path ...{self.partial_path} {Notes.time()}', 'green'))

    def delete(self):
        if not os.path.exists(self.folder_path):
            print(Notes.colored(f'Path does not exist.. Take a screenshot to initiate the path...', 'red'))
            return False

        if len(os.listdir(self.folder_path)) == 0:
            print(Notes.colored(f'Path does not have any file.. Take a screenshot to initiate the path...', 'red'))
            return False
        
        file_list = os.listdir(self.folder_path)
        sorted_file_list = sorted(file_list, key=lambda x: os.path.getmtime(os.path.join(self.folder_path, x)))

        try:
            os.remove(os.path.join(self.folder_path, sorted_file_list[-1]))
        except Exception as e:
            print(Notes.colored(e, 'red'))

        print(Notes.colored(f'Removed {sorted_file_list[-1]} from path ...{self.partial_path} {Notes.time()}', 'green'))

    def playaudio(self, file):
        try:
            pass
        except:
            pass

    def on_press(self, key):
        if key == Key.f2:
            self.screenshot()
            if self.args.audio_on: self.playaudio('effect-1')

        elif key == Key.f4:
            self.delete()
            if self.args.audio_on: self.playaudio('effect-1')

        elif key == Key.f7:
            self.folder_path = input('Please enter the desired path: ')
            self.store('Last_Path', self.folder_path)

            print(Notes.colored(f'Folder path successfully switched to {self.folder_path}... {Notes.time()}', 'green'))
            self.partial_path = self.set_partial_path()

        elif keyboard.is_pressed(('ctrl', 'shift', 'c')):
            os._exit(0)

    @staticmethod
    def time():
        return f'({datetime.now().strftime("%H:%M:%S")})'
    
    @staticmethod
    def colored(s, color):
        if color == 'green':
            return f'\033[1;32m {s} \033[0m'
        
        elif color == 'red':
            return f'\033[91m {s} \033[0m'
        
        elif color == 'blue':
            return f'\033[34m {s} \033[0m'
        
        else:
            return s


if __name__ == '__main__':

    with Listener(on_press=Notes().on_press) as lst:
        lst.join()