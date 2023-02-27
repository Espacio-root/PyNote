from datetime import datetime
import json
import os
from PIL import ImageGrab
from playsound import playsound
from pynput.keyboard import Listener, Key
import argparse

class Notes:

    def __init__(self, folder_path='') -> None:

        parser = argparse.ArgumentParser()
        parser.add_argument("--path", default=False)
        parser.add_argument("--default-path", default=False)
        parser.add_argument("--audio-on", default=False, action="store_true")
        parser.add_argument("--last-path", default=False, action="store_true")
        self.args = parser.parse_args()

        if self.args.default_path:
            self.store('Path', self.args.default_path)

        if folder_path == '':
            
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
                print(f'Path was not specified, hence files are being cached at {self.folder_path}')

        else:
            self.folder_path = folder_path
        self.store('Last_Path', self.folder_path)

    def partial_path(self):
        
        if os.getcwd().split('\\')[-1] in self.folder_path:
            return self.folder_path.split(os.getcwd().split('\\')[-1])[-1]
        else:
            return self.folder_path.split("\\")[-1]

    def store(self, key, value):

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
                cur = int([elem for elem in sorted(os.listdir(self.folder_path), key= lambda x: int(x.split('.')[0])) if elem.endswith('png')][-1].split('.')[0]) + 1
            except: cur = 1
        else:
            os.makedirs(self.folder_path)
            cur = 1

        im.save(fr'{self.folder_path}\{cur}.png')
        print(f'Stored {cur}.png at path ...{self.partial_path()}')

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

        print(f'Removed {sorted_file_list[-1]} from path ...{self.partial_path()}')

    def playaudio(self, file):
        try:
            playsound(fr'{os.getcwd()}\assets\audio\{file}.mp3')
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

            print(f'Folder path successfully switched to {self.folder_path}...')


if __name__ == '__main__':

    with Listener(on_press=Notes().on_press) as lst:
        lst.join()