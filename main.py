import kivy
import logFunc

kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

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
    def __init__(self):
        # Constant part of image path
        self.photo_path = ""
        self.current_photo = 0

    def next_photo(self):
        self.current_photo += 1
        return self.photo_path + str(self.current_photo) + ".jpg"

class ScreenSettingLeft(Screen):
    pass

class ScreenMatchesRight(Screen):
    pass


# The ScreenManager controls moving between screens
screen_manager = ScreenManager()

# Add the screens to the manager and then supply a name
# that is used to switch screens
screen_manager.add_widget(ScreenLogin(name="screen_login"))
screen_manager.add_widget(ScreenMainMid(name="screen_main_mid"))
screen_manager.add_widget(ScreenSettingLeft(name="screen_setting_left"))
screen_manager.add_widget(ScreenMatchesRight(name="screen_matches_right"))


class FacebookGirlsApp(App):

    def build(self):
        logFunc.logFunc("")
        return screen_manager


fbg_app = FacebookGirlsApp()
fbg_app.run()