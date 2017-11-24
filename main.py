import kivy
from logFunc import logFunc
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.uix.screenmanager import WipeTransition



kivy.require('1.9.1')
# You can create your kv code in the Python file
Builder.load_file("res/ScreenLogin.kv")
Builder.load_file("res/ScreenMainMid.kv")
Builder.load_file("res/ScreenSettingLeft.kv")
Builder.load_file("res/ScreenMatchesRight.kv")


# Create a class for all screens in which you can include
# helpful methods specific to that screen
class ScreenLogin(Screen):
    def verify(self):
        if logFunc(password=self.ids.in_pass.text, username=self.ids.in_pass.text, directory="assets/myfriends/"):
            self.screen_manager.transition = WipeTransition()
            self.screen_manager.transition.duration = 1
            self.screen_manager.current = 'screen_main_mid'
        else:
            button = Button(text='Try again!', size=(175, 50), size_hint=(None, None), pos_hint={"center_y": .5})
            popup = Popup(title='Authentication failed!', content=button,
                          size_hint=(None, None), size=(200, 120))
            button.bind(on_press=popup.dismiss)
            popup.open()


class ScreenMainMid(Screen):

    img_path = "assets/myfriends/0.jpg"

    def __init__(self, **kwargs):
        super(ScreenMainMid, self).__init__(**kwargs)
        self.photo_path = "assets/myfriends/"
        self.current_photo = 0

    def next_photo(self):
        self.current_photo += 1
        return self.img_path + str(self.current_photo) + ".jpg"

    def loadPicture(self):
        self.ids.img.source = self.next_photo()
        self.ids.img.reload()
        self.do_layout()

class ScreenSettingLeft(Screen):
    pass

class ScreenMatchesRight(Screen):
    pass



screen_manager = ScreenManager()


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