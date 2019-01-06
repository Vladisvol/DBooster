import win32ui
import win32gui
import win32con
import win32api
import PIL
import pywintypes
import easygui
import zipfile
import os
import ctypes
import ctypes.util

from shutil import copyfile

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.uix.filechooser import FileChooserIconView
from kivy.config import Config

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

from kivy.core.window import Window
from kivy.core.text import LabelBase

LabelBase.register(name = 'FiraSansExtraCondensed', fn_regular = 'FiraSansExtraCondensed-Regular.ttf')
Window.clearcolor = (.94, .94, .94, 1)

class MainScreen(Screen):
    pass

class AnotherScreen(Screen):
    def file(self):
        with open('counter.txt', 'r') as f:
            if int(f.read()) >= 49:
                
                content = GridLayout(
                    cols = 1,
                    rows = 2
                    )

                content.add_widget(Label(text = 'You can\'t add more than 49 apps!'))
                button = Button(
                    text = 'Got it!',
                    size_hint = (None, None),
                    size = (200, 50)
                    )
                content.add_widget(button)

                popup = Popup(
                    content = content,
                    title = 'Attention',
                    size_hint = (None, None),
                    size = (400, 400)
                    )

                button.bind(on_press = popup.dismiss)

                popup.open()
            else:    
                try:
                    file_open = easygui.fileopenbox() # For example E:\...\someapp.exe

                    f = list(file_open)
                    f.reverse()

                    i = 0

                    while i <= len(f):  # E:\...\someapp.exe => E:\...\someapp
                        if f[i] == '.':
                            f = f[i+1:]
                            f.reverse()
                            f = ''.join(f)
                            i = 0
                            break
                        i += 1

                    f = list(f)
                    part = f
                    f.reverse()

                    while i <= len(f):  # E:\...\someapp.exe => E:\...\
                        if f[i] == '\\':
                            f = f[i:]
                            f.reverse()
                            f = ''.join(f)
                            i = 0
                            break
                        i += 1

                    while i <= len(part):  # E:\...\someapp.exe => someapp
                        if part[i] == '\\':
                            part = part[:i]
                            part.reverse()
                            folder = ''.join(part)
                            del i
                            break
                        i += 1

                    directory = f + folder # E:\...\ + someapp = E:\...\someapp\
                except:
                    pass

                try:
                    os.mkdir(directory)
                except:
                    pass

                try:   
                    file_open = file_open.replace("\\", "/")
                    icoX = win32api.GetSystemMetrics(win32con.SM_CXICON)
                    icoY = win32api.GetSystemMetrics(win32con.SM_CXICON)

                    large, small = win32gui.ExtractIconEx(file_open, 0)
                    win32gui.DestroyIcon(small[0])

                    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
                    hbmp = win32ui.CreateBitmap()
                    hbmp.CreateCompatibleBitmap(hdc, icoX, icoX)
                    hdc = hdc.CreateCompatibleDC()

                    hdc.SelectObject(hbmp)
                    hdc.DrawIcon((0, 0), large[0])

                    from PIL import Image
                    bmpstr = hbmp.GetBitmapBits(True)
                    img = Image.frombuffer(
                        'RGBA',
                        (32,32),
                        bmpstr, 'raw', 'BGRA', 0, 1
                        )

                    icon_dir = directory + '\\icon.png'
                    icon_dir = icon_dir.replace('\\', '/')
                    img.save(icon_dir)
                
                    with open('counter.txt', 'r') as counter:
                        cnt = int(counter.read())

                    with open('main.kv', 'a') as kv:
                        kv.write('''
        Button:
            background_normal: \'''' +  icon_dir + '''\'
            size_hint: (None, None)
            size: (32, 32)
            on_press: root.run(\'''' + file_open + '''\')
''')
                    with open('counter.txt', 'w') as counter:
                        counter.write(str(cnt + 1))
                    self.restart()
                except:
                    pass

    def run(self, link):
        try:
            os.startfile(link)
        except:
            pass

    def restart(self):
        os.startfile('main.py')
        os.abort()

class ASCopy(AnotherScreen):
    pass

class ScreenManagement(ScreenManager):
    pass

Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        self.title = 'DBooster'
        with open('counter.txt', 'r') as counter:
            cnt = int(counter.read())

        if cnt > 0:
            return AnotherScreen()

MainApp().run()