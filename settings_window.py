from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import csv

class SettingsWindow(Screen):
    current_user = StringProperty("")

    def show_popup(self, title, text):
        popup = Popup(title=title, content=Label(text=text), size_hint=(None, None), size=(400, 200))
        popup.open()

    def on_open(self):
        self.ids.username.text = self.current_user

    
    def go_back(self): 
        self.ids.username.text = ""
        main_screen = self.manager.get_screen('main')
        main_screen.current_user = self.current_user
        self.manager.current = 'main'


    def change_settings(self):
        if(self.ids.username.text == self.current_user):
            self.change_password()
            return
        self.change_username()
        self.change_password()

    def change_username(self):
        try:
            new_username = self.ids.username.text
            if not new_username:
                self.show_popup("Kļūda", "Lūdzu ievadiet jaunu lietotājvārdu")
                return

            users_data = []
            username_taken = False

            with open('users.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                for row in reader:
                    if row['username'] == new_username:
                        username_taken = True
                        break
                    users_data.append(row)

            if username_taken:
                self.show_popup("Kļūda", "Lietotājvārds jau ir aizņemts")
                return
            
            users_data = []
            with open('users.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                for row in reader:
                    if row['username'] == self.current_user:
                        row['username'] = new_username
                    users_data.append(row)

            with open('users.csv', 'w', encoding='utf-8', newline='') as file:
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='\t')
                writer.writeheader()
                writer.writerows(users_data)

            self.show_popup("Veiksmīgi", "Lietotājvārds veiksmīgi nomainīts!")
        except Exception as e:
            self.show_popup("Kļūda", f"Neizdevās nomainīt lietotājvārdu: {str(e)}")

    def change_password(self):
        try:
            new_password = self.ids.new_password.text
            if not new_password:
                self.show_popup("Kļūda", "Lūdzu ievadiet jaunu paroli")
                return
            users_data = []
            with open('users.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                for row in reader:
                    if row['username'] == self.current_user:
                        row['password'] = new_password
                    users_data.append(row)
            with open('users.csv', 'w', encoding='utf-8', newline='') as file:
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='\t')
                writer.writeheader()
                writer.writerows(users_data)
            self.show_popup("Veiksmīgi", "Parole veiksmīgi nomainīta!")
        except Exception as e:
            self.show_popup("Kļūda", f"Neizdevās nomainīt paroli: {str(e)}")