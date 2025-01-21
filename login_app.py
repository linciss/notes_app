from kivy.app import App  
from kivy.core.window import Window 
from kivy.utils import platform 
from kivy.config import Config  
from kivy.uix.screenmanager import ScreenManager

import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

Config.set('input', 'mouse', 'mouse, multitouch_on_demand')

Config.set('kivy', 'mouse cursor enable', 1)
Config.write() 

from login_window import LoginWindow
from main_window import MainWindow
from settings_window import SettingsWindow
from note_editor import NoteEditor
from note_preview import NotePreview

class WindowManager(ScreenManager):
    pass

class LoginApp(App):

    def build(self):
        if platform not in ('android', 'ios'):
            Window.size = (400, 600)


        if platform in ('android', 'ios'):
            Window.fullscreen = 'auto'

        return WindowManager()


if __name__ == '__main__':
    LoginApp().run()