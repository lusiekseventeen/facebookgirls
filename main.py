import kivy
import requests
from logFunc import login
from logFunc import Girl
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
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

#Czcionka
LabelBase.register(name="klavika", fn_regular="assets/fonts/klavika.otf")

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

    label1 = Label(text="we're getting your girls", font_name="klavika")
    label2 = Label(text="almost done", font_name="klavika")
    label3 = Label(text="yup! we've got them!", font_name="klavika")
    popup = Popup(title='please wait...', content=label1, size_hint=(None, None), size=(400, 400))
    animation = Animation(color=(1,1,1,1), duration=1)

    def verify(self):
        session = requests.session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
        })
        if login(session, email=self.ids.in_login.text, password=self.ids.in_pass.text, array=all_my_girls):
            self.navToMainMid()
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

    def animateWaitScreen(self, l1):
        for x in range(20):
            self.animation += Animation(color=(1, 1, 1, .2), duration=1, t="in_back")
            self.animation += Animation(color=(1, 1, 1, 1), duration=1, t="in_back")
        self.animation.start(l1)


    def waitScreenStart(self):
        self.popup.open()
        self.animateWaitScreen(self.label1)

    def waitScreenStop(self):
        self.popup.dismiss()
        self.animation.cancel(self.label1)

    def navToMainMid(self):
        screen_manager.transition = WipeTransition()
        screen_manager.transition.duration = 1
        screen_manager.current = "screen_main_mid"


class ScreenMainMid(Screen):

    img_path = "assets/myfriends/0.jpg"

    yes_path = "assets/yes.png"
    no_path = "assets/no.png"
    yes_path_prompt = "assets/yes_pressed.png"
    no_path_prompt = "assets/no_pressed.png"

    path = "assets/myfriends/"

    current_girl = 0

    def __init__(self, **kwargs):
        super(ScreenMainMid, self).__init__(**kwargs)
        #self.downloadFirst3()
        self.loadFirst()

    def no(self):
        self.loadPicture()

    def yes(self):
        self.loadPicture()

    def downloadFirst3(self):
        if (self.current_girl == 0):
            for x in range(3):
                if len(all_my_girls) > x + 1:
                    all_my_girls[self.current_girl].download_picture()

    def loadFirst(self):
        if len(all_my_girls) > 0:
            self.ids.img.source = self.next_photo()
            self.ids.img.reload()
            self.do_layout()
        else:
            self.ids.img.source = "assets/matches.png"
            self.ids.img.reload()
            self.do_layout()

    def next_photo(self):
        self.current_girl += 1
        #dynamiczne pobieranie do przodu
        if len(all_my_girls) > self.current_girl + 1:
            for x in range(3):
                if len(all_my_girls) > x + 1:
                   if all_my_girls[self.current_girl+x].path == "":
                       all_my_girls[self.current_girl].download_picture()

            return all_my_girls[self.current_girl].path
        else:
            return "assets/matches.png"

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
        self.putPictures()

    def putPictures(self):
        #curdir = dirname(__file__)
        for girl in matches:
            try:
                picture = Picture(source=girl.path, rotation=randint(-30, 30))
                self.images_holder.add_widget(picture)
            except Exception as e:
                Logger.exception('Pictures: Unable to load <%s>' % girl)

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




screen_manager = ScreenManager()

#Menadzer ekranow
screen_manager.add_widget(ScreenLogin(name="screen_login"))
screen_manager.add_widget(ScreenMainMid(name="screen_main_mid"))
screen_manager.add_widget(ScreenSettingLeft(name="screen_setting_left"))
screen_manager.add_widget(ScreenMatchesRight(name="screen_matches_right"))



class FacebookGirlsApp(App):

    def build(self):
        return screen_manager

    screen_manager.current = "screen_login"


fbg_app = FacebookGirlsApp()
fbg_app.run()