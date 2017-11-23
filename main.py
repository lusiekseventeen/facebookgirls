import kivy
#import logFunc

kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.properties import StringProperty

# You can create your kv code in the Python file
Builder.load_file("res/ScreenLogin.kv")
Builder.load_file("res/ScreenMainMid.kv")
Builder.load_file("res/ScreenSettingLeft.kv")
Builder.load_file("res/ScreenMatchesRight.kv")


# Create a class for all screens in which you can include
# helpful methods specific to that screen
class ScreenLogin(Screen):
    pass


class ScreenMainMid(Screen):

    img_path = ""

    def __init__(self, **kwargs):
        super(ScreenMainMid, self).__init__(**kwargs)
        self.img_source = "assets/logo.png"

    def next_photo(self):
        self.current_photo = 0
        return self.photo_path + str(self.current_photo) + ".jpg"

    def loadPicture(self):
        self.img_path = StringProperty("assets/myfriends/test.jpg")



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