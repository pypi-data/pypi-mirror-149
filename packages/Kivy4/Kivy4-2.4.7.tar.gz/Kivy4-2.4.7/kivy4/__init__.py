import time, pyperclip, os, darkdetect, threading
from kivy import Config
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

Config.set('graphics', 'resizable', 0)
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
Config.set('kivy', 'exit_on_escape', 0)
Config.write()

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.settings import ContentPanel
from kivymd.app import MDApp
from screeninfo import get_monitors
from kivy.properties import *


class Content(BoxLayout):
    pass


def icons(f: str = ''):
    from kivymd.icon_definitions import md_icons
    print([x for x in list(md_icons.keys()) if f in x])


def getSpec(name: str, icon: str = 'icon.ico', filename: str = 'main.py', path: str = os.getcwd()):
    path = path.replace("\\", r"\\")

    with open(filename.replace('.py', '.spec'), 'w') as f:
        f.write(fr"""from kivy_deps import sdl2, glew

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['{filename}'],
             pathex=['{path}'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={{}},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='{name}',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None, icon='{icon}')

coll = COLLECT(exe, Tree('{path}'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='{name}')""")


def thread(func):
    def inner(*args, **kwargs):
        threading.Thread(target=lambda: func(*args, **kwargs), daemon=True).start()

    return inner


def tic(func):
    def inner(*args, **kwargs):
        tic = time.perf_counter()
        func(*args, **kwargs)
        toc = time.perf_counter()

        print(f'Duration of {func.__name__}: {round(toc - tic, 8)}')

    return inner


class Kivy4(MDApp):
    dark_mode_icon = StringProperty('')

    def __init__(self, string: str = '', app_name: str = '', dict_of_files: dict = None,
                 screen_size=None, minimum=None, center: bool = True,
                 sun_icon: str = 'white-balance-sunny', moon_icon: str = 'weather-night',
                 main_color: str = 'Blue', icon: str = '', toolbar=False, app_data: bool = True,
                 disable_x: bool = False, pre_string: str = '', **kwargs):

        super().__init__(**kwargs)

        if minimum is None:
            minimum = [0.1, 0.1]

        self.app_name = app_name
        self.builder_string = '''<Content>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "100dp"'''

        if app_data:
            app_data_path = os.getenv('APPDATA') + '/' + app_name
            self.appdata_path = app_data_path
            self.create_files(dict_of_files)

            self.moon_icon = moon_icon
            self.sun_icon = sun_icon
            self.isDarkMode()

        self.dialog = None
        self.setProperties(main_color, icon, toolbar, string, pre_string)
        self.disable_x = disable_x

        screen = get_monitors()[0]
        self.width = screen.width
        self.height = screen.height

        self.screen_positions(screen_size, minimum, center)

        self.run()

    def setProperties(self, main_color, icon, toolbar, string, pre_string):

        for x in pre_string.split('\n'):
            if 'x,y=' in x.replace(' ', '') and '#' not in x:
                self.builder_string += '\n' + self.x_y(x)

            else:
                self.builder_string += '\n' + x

        self.builder_string += self.custom_classes()

        if toolbar:
            self.builder_string += self.getToolbar(toolbar)

            for x in string.split('\n'):
                if 'x,y=' in x.replace(' ', '') and '#' not in x:
                    self.builder_string += '\n            ' + self.x_y(x)

                else:
                    self.builder_string += '\n            ' + x

        self.theme_cls.primary_palette = main_color
        self.icon = icon

    def build(self):
        self.use_kivy_settings = False
        self.settings_cls = ContentPanel
        self.title = self.app_name

        Window.bind(on_dropfile=lambda *args: self.on_drop_file(*args),
                    on_request_close=lambda x: self.on_request_close(self.disable_x))

        self.Build()
        return Builder.load_string(self.builder_string)

    def Build(self):
        pass

    def screen_positions(self, screen_size, minimum=None, center=True):

        if minimum is None:
            minimum = [0.1, 0.1]

        min_x, min_y = minimum

        if screen_size is None:
            x, y = 0.6, 0.6

        else:
            x, y = screen_size[0], screen_size[1]

        if x <= 1 or y <= 1:
            Window.size = (self.width * x, self.height * y)
            Window.minimum_height = self.height * min_y
            Window.minimum_width = self.width * min_x


        else:
            Window.size = (x, y)
            Window.minimum_height = min_y
            Window.minimum_width = min_x

            if center:
                Window.left = (self.width - x) / 2
                Window.top = (self.height - y) / 2
                return

            else:
                return

        if center:
            Window.left = (self.width - (self.width * x)) / 2
            Window.top = (self.height - (self.height * y)) / 2

    def create_files(self, list_of_files):
        try:
            if not os.path.isdir(self.appdata_path):
                os.mkdir(self.appdata_path)

            if list_of_files:
                for file in list_of_files:
                    self.setFile(file, list_of_files[file])

        except Exception as e:
            return e

    def setFile(self, file, value, extension='.txt'):
        path_to_create = f'{self.appdata_path}/{file}{extension}'

        try:
            with open(path_to_create, 'w') as f:
                f.write(value)

        except Exception as e:
            print(e)
            return e

    def getFile(self, file, default=None, create_file_if_not_exist=False, extension='.txt'):
        path_of_file = f'{self.appdata_path}/{file}{extension}'

        try:
            with open(path_of_file, 'r') as f:
                return f.read()

        except FileNotFoundError:
            if create_file_if_not_exist:
                with open(path_of_file, 'w') as f:
                    f.write(default)
                    return default

            else:
                return default

        except Exception as e:
            print(e)
            return default

    def isDarkMode(self, filename='dark mode.txt'):
        try:
            with open(self.appdata_path + '/' + filename, 'r') as f:
                current_mode = f.read()
                self.setDarkModeIcon(current_mode)

                return current_mode == 'Dark'

        except FileNotFoundError:
            with open(self.appdata_path + '/' + filename, 'w') as f:
                default = darkdetect.theme()
                f.write(default)

                self.setDarkModeIcon(default)

                return default == 'Dark'

        except AttributeError:
            return False

    def setDarkMode(self, value=None, filename='dark mode'):
        if value is None:
            value = darkdetect.theme()

        self.setFile(filename, value)
        self.setDarkModeIcon(value)

    def reverseDarkMode(self, filename: str = 'dark mode.txt'):
        try:
            with open(self.appdata_path + '/' + filename, 'r') as f:
                current_mode = f.read()

                if current_mode == 'Dark':
                    self.setDarkMode('Light')
                    return 'Light'

                self.setDarkMode('Dark')
                return 'Dark'

        except FileNotFoundError:
            with open(self.appdata_path + '/' + filename, 'w') as f:
                default = darkdetect.theme()
                f.write(default)

                self.setDarkModeIcon(default)

                return default

        except AttributeError:
            return False

    def setDarkModeIcon(self, value):
        if value == 'Dark':
            self.dark_mode_icon = self.moon_icon

        else:
            self.dark_mode_icon = self.sun_icon

        self.theme_cls.theme_style = value

    def getToolbar(self, properties: list):
        if properties == True:
            right_icons, left_icons, name = '[[app.dark_mode_icon, lambda x: app.reverseDarkMode()]]', '[]', self.app_name

        elif len(properties) == 2:
            left_icons, right_icons, name = properties[0], properties[1], self.app_name
            name = self.app_name

        else:
            left_icons, right_icons, name = properties


        return f'''
Screen:
    MDToolbar:
        id: toolbar
        pos_hint: {{"top": 1}}
        elevation: 10
        title: "{name}"
        right_action_items: {right_icons}
        left_action_items: {left_icons}

    MDNavigationLayout:
        x: toolbar.height
        ScreenManager:
            id: screen_manager
'''

    @staticmethod
    def toast(text, duration=2.5):
        from kivymd.toast import toast

        toast(text=text, duration=duration)

    @staticmethod
    def snack(text, button_text=None, func=None):
        from kivymd.uix.button import MDFlatButton
        from kivymd.uix.snackbar import Snackbar

        snack = Snackbar(text=text)

        if func and button_text:
            snack.buttons = [MDFlatButton(text=f"[color=#1aaaba]{button_text}[/color]", on_release=func)]

        snack.open()

    @staticmethod
    def x_y(x_y):
        x, y = eval(x_y.split("=")[1])
        return f"{x_y.index('x') * ' '}pos_hint: {{'center_x': {x}, 'center_y': {y}}}"

    @staticmethod
    def custom_classes():
        return '''
<Text@MDLabel>:
    halign: 'center'
    font_name: 'arial'

<Input@MDTextField>:
    mode: "rectangle"
    text: ""
    size_hint_x: 0.5
    font_name: 'arial'

<Check@MDCheckbox>:
    group: 'group'
    size_hint: None, None
    size: dp(48), dp(48)

<Btn@MDFillRoundFlatButton>:
    text: ""
    font_name: 'arial'

<BtnIcon@MDFillRoundFlatIconButton>:
    text: ""
    font_name: 'arial'

<Img@Image>:    
    allow_stretch: True

<CircleIcon@MDFloatingActionButton>:
    md_bg_color: app.theme_cls.primary_color
'''

    def on_drop_file(self, *args):
        print(*args)

    @staticmethod
    def on_request_close(disable_x: bool = False):
        return disable_x

    @thread
    def write_to_clipboard(self, text: str):
        pyperclip.copy(text)

    def show_date_picker(self, on_save, mode='picker'):
        from kivymd.uix.picker import MDDatePicker
        date_dialog = MDDatePicker(mode=mode)
        date_dialog.bind(on_save=on_save, on_cancel=self.on_cancel_picker)
        date_dialog.open()

    def on_cancel_picker(self, instance, value):
        pass

    def popup_kivy4(self, title='My popup', content=Content(), cancel_text='CANCEL', okay_text='OKAY',
              okay_func=lambda *args: print('yes'), cancel_func=None):

        if cancel_func is None:
            cancel_func = lambda *args: self.dismiss()

        if not self.dialog:
            self.dialog = MDDialog(
                title=title,
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text=cancel_text,
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press=cancel_func
                    ),
                    MDFlatButton(
                        text=okay_text,
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press=okay_func
                    ),
                ],
            )

        self.dialog.open()

    def dismiss(self):
        try:
            self.dialog.dismiss()

        except Exception as e:
            print(e)