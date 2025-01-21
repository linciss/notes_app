from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
import csv
import os

class LoginWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    id = StringProperty("")

    def verify_user(self, username, password):
        try:
            if os.path.exists('users.csv'):
                with open('users.csv', 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter='\t')
                    for row in reader:
                        if row['username'] == username and row['password'] == password:
                            self.id = row['user_id']
                            return True
        except Exception as e:
            print(f"Error: {e}")
        return False
    

    def login_button(self):

        if self.verify_user(self.username.text, self.password.text):
            print("Login successful!")

            main_screen = self.manager.get_screen('main')
            main_screen.ids.notes.clear_widgets()
            main_screen.current_user = self.username.text
            main_screen.id = self.id
            main_screen.update_welcome_text()
            self.username.text = ''
            self.password.text = ''
            self.manager.current = 'main'
        else:
            print("Login failed!")