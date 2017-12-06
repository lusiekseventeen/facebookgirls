import kivy
from logFunc import logFunc
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.uix.screenmanager import WipeTransition
from kivy.uix.listview import ListItemButton
from glob import glob
from random import randint
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.core.text import LabelBase


kivy.require('1.9.1')

Builder.load_file("res/ScreenLogin.kv")
Builder.load_file("res/ScreenMainMid.kv")
Builder.load_file("res/ScreenSettingLeft.kv")
Builder.load_file("res/ScreenMatchesRight.kv")
#Builder.load_file("res/MatchItem.kv")


class MatchItem(BoxLayout):
    def __init__(self, **kwargs):
        super(ScreenMainMid, self).__init__(**kwargs)
        self.current_photo = 0

class Picture(Scatter):
    source = StringProperty(None)


class ScreenLogin(Screen):
    def verify(self):
        if logFunc(password=self.ids.in_pass.text, username=self.ids.in_login.text, directory="assets/myfriends/"):
            screen_manager.transition = WipeTransition()
            screen_manager.transition.duration = 1
            screen_manager.current = "screen_main_mid"
        else:
            button = Button(text='Try again!', size=(175, 50), size_hint=(None, None), pos_hint={"center_y": .5})
            popup = Popup(title='Authentication failed!', content=button,
                          size_hint=(None, None), size=(200, 120))
            button.bind(on_press=popup.dismiss)
            popup.open()
            screen_manager.transition = WipeTransition()
            screen_manager.transition.duration = 1
            screen_manager.current = 'screen_main_mid'


class ScreenMainMid(Screen):

    img_path = "assets/myfriends/0.jpg"
    path = "assets/myfriends/"

    def __init__(self, **kwargs):
        super(ScreenMainMid, self).__init__(**kwargs)
        self.current_photo = 0

    def next_photo(self):
        self.current_photo += 1
        return self.path + str(self.current_photo) + ".jpg"

    def likeher(self):
        matches.append(current_girl)
        #nextGirl()
        self.loadPicture()

    def loadPicture(self):
        self.ids.img.source = self.next_photo()
        self.ids.img.reload()
        self.do_layout()

    #TODO: nastepna dziewucha zamiast nastepnego zdjecia.
    #def nextGirl(self):
        #current_girl =

class ScreenSettingLeft(Screen):
    pass

class ScreenMatchesRight(Screen):

    def __init__(self, **kwargs):
        super(ScreenMatchesRight, self).__init__(**kwargs)
        self.current_photo = 0
        self.putPictures()

    def putPictures(self):
        curdir = dirname(__file__)
        screen_manager.transition = WipeTransition()
        screen_manager.transition.duration = 1
        screen_manager.current = "screen_login"
        for filename in glob(join(curdir, 'assets/myfriends', '*')):
            try:
                # load the image
                picture = Picture(source=filename, rotation=randint(-30, 30))
                # add to the main field
                self.add_widget(picture)
            except Exception as e:
                Logger.exception('Pictures: Unable to load <%s>' % filename)

class Girl():
    id = 0
    name = ""
    photo_url = ""

    def __init__(self,id, name, photo_url):
        self.id = id
        self.name = name
        self.photo_url = photo_url

#TODO Pobrane dziewuchy klasy Girls() wrzucic do tej listy
all_my_girls = []
#list tych dziewuch ktore sie podobaja
matches = []

test_girl = Girl(0, "Ala", "assets/myfriends/0.jpg")
current_girl = test_girl
matches.append(test_girl)


screen_manager = ScreenManager()

#Menadzer ekranow
screen_manager.add_widget(ScreenLogin(name="screen_login"))
screen_manager.add_widget(ScreenMainMid(name="screen_main_mid"))
screen_manager.add_widget(ScreenSettingLeft(name="screen_setting_left"))
screen_manager.add_widget(ScreenMatchesRight(name="screen_matches_right"))

#Czcionka
LabelBase.register(name="klavika", fn_regular="assets/fonts/klavika.otf")


class FacebookGirlsApp(App):

    def build(self):
        return screen_manager

    screen_manager.current = "screen_login"


fbg_app = FacebookGirlsApp()
fbg_app.run()