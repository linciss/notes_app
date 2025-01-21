from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import csv

class SettingsWindow(Screen):
    current_user = StringProperty("")

    def show_popup(self, title, text):
        popup = Popup(title=title, content=Label(text=text), size_hint=(None, None), size=(400, 200))
        popup.open()

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