import kivy
import requests
from logFunc import login
from logFunc import Girl
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
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
from kivy.animation import Animation
from kivy.properties import ObjectProperty
from sklearn import svm


kivy.require('1.9.1')

Builder.load_file("res/ScreenLogin.kv")
Builder.load_file("res/ScreenMainMid.kv")
Builder.load_file("res/ScreenSettingLeft.kv")
Builder.load_file("res/ScreenMatchesRight.kv")
#Builder.load_file("res/MatchItem.kv")

all_my_girls = []
training_set = []
matches = []
main_classifier = svm.SVC(gamma=0.001)

class MatchItem(BoxLayout):
    def __init__(self, **kwargs):
        super(ScreenMainMid, self).__init__(**kwargs)
        self.current_photo = 0


class Picture(Scatter):
    source = StringProperty(None)


class ScreenLogin(Screen):
    def verify(self):
        session = requests.session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
        })
        if login(session, email=self.ids.in_login.text, password=self.ids.in_pass.text, array=all_my_girls):
            screen_manager.transition = WipeTransition()
            screen_manager.transition.duration = 1
            screen_manager.current = "screen_main_mid"
        else:
            button = Button(text='Try again!', size=(175, 50), size_hint=(None, None), pos_hint={"center_y": .5})
            popup = Popup(title='Authentication failed!', content=button,
                          size_hint=(None, None), size=(200, 120))
            button.bind(on_press=popup.dismiss)
            popup.open()

    def animate(self, instance):
        animation = Animation(size=(instance.width + 5, instance.height + 5), duration=0.1)
        animation += Animation(size=(instance.width, instance.height), duration=0.1)
        animation.start(instance)


class ScreenMainMid(Screen):

    img_path = "assets/myfriends/0.jpg"

    yes_path = "assets/yes.png"
    no_path = "assets/no.png"
    yes_path_prompt = "assets/yes_pressed.png"
    no_path_prompt = "assets/no_pressed.png"

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

    def animate(self, instance):
        animation = Animation(size=(instance.width+5, instance.height+5), duration=0.1)
        animation += Animation(size=(instance.width, instance.height), duration=0.1)
        animation.start(instance)

    #Podpowiedz na TAK
    def putYesPrompt(self):
        self.ids.btn_decide_yes.source = self.yes_path_prompt
        self.ids.btn_decide_yes.reload()
        self.do_layout()

    # Podpowiedz na NIE
    def putNoPrompt(self):
        self.ids.btn_decide_no.source = self.no_path_prompt
        self.ids.btn_decide_no.reload()
        self.do_layout()

    #Reset podpowiedzi
    def resetPrompt(self):
        self.ids.btn_decide_no.source = self.no_path
        self.ids.btn_decide_no.reload()
        self.ids.btn_decide_yes.source = self.yes_path
        self.ids.btn_decide_yes.reload()
        self.do_layout()

    #TODO: nastepna dziewucha zamiast nastepnego zdjecia.
    #def nextGirl(self):
        #current_girl =

class ScreenSettingLeft(Screen):
    pass

class ScreenMatchesRight(Screen):

    images_holder = ObjectProperty()

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
                picture = Picture(source=filename, rotation=randint(-30, 30))
                self.images_holder.add_widget(picture)
            except Exception as e:
                Logger.exception('Pictures: Unable to load <%s>' % filename)
    def alignAll(self):
        #photo
        for child in self.images_holder.children:
            animation = Animation(rotation=child.rotation + randint(-30,30), duration=0.2)
            animation &= Animation(pos=(200, 200), scale=1, t='out_circ', duration=0.3)
            animation.start(child)

    def animate(self, instance):
        animation = Animation(size=(instance.width+5, instance.height+5), duration=0.1)
        animation += Animation(size=(instance.width, instance.height), duration=0.1)
        animation.start(instance)


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