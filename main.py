from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from datetime import datetime
import glob
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file('design.kv')
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
        #print("Sign up button")
        #SignUpScreen
    def login(self, uname, pword):
        with open("users.json", "r") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = 'login_screen_success'
        else:
            self.ids.login_wrong.text = "Wrong level of hating"



class RootWidget(ScreenManager):
    pass


class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        try:
            with open("users.json", "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, create an empty dictionary
            users = {}
        except json.JSONDecodeError:
            # If the file is not valid JSON, handle the error gracefully
            print("Error: users.json is not valid JSON. Please check the file contents.")
            return

        users[uname] = {'username': uname, 'password': pword, 'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        # Now, you can write the updated user data back to the file
        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)  # Dump the updated user data back to the file

        print("User added successfully:", users[uname])
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.current = 'right'
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'

    def get_quote(self, feel):
        feel = feel.lower()
        available_files = glob.glob("quotes/*txt")
        print(available_files)
        available_feelings = [Path(filename).stem for filename in available_files]
        print(available_feelings)
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt", encoding = "utf-8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "we only happy, sad or unloved over here"

class ImageButton(ButtonBehavior, HoverBehavior, Image ):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()
