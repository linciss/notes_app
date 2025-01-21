from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import os
import csv
import re

class NoteEditor(Screen):
    user_id = StringProperty("")
    note = ObjectProperty(None)
    color = ObjectProperty(None)
    edit = False
    note_id = StringProperty("")
    # catgeory = ObjectProperty(None)


    def create_note(self):
        
        
        note = self.ids.note.text
        color = self.ids.color.text
        if(color == ""):
            color = "#FFFFFF"
        
        if len(color) != 7 or color[0] != "#":
            self.show_popup("Error", "Ievadi hex kodu ar # zīmi priekšā vai pārbaudi vai ir 7 simboli") 
            return
        
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)

        if not match:
            self.show_popup("Error", "Ievadi pareizu hex kodu")
            return

        if(self.edit):
            self.edit_note(note, color)
            return

        try:
            if note:
                with open('notes.csv', 'a', encoding='utf-8', newline='') as file:
                    file.write(f"{self.get_row_count()},{self.user_id},{note},{color}\n")
                self.ids.note.text = ""
                self.ids.color.text = ""
                self.edit = False
                self.manager.current = 'main'
            else:
                self.show_popup("Error", "Ievadi tekstu")
        except Exception as e:
            self.show_popup("Error", f"Error: {str(e)}")
            


    def go_back(self): 
        self.edit = False
        self.manager.current = 'main'
       
    def get_row_count(self):
        try:
            if os.path.exists('notes.csv'):
                with open('notes.csv', 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    row_count = sum(1 for row in reader)
                    print(row_count)
                    return row_count
        except Exception as e:
            self.show_popup("Error", f"Error: {str(e)}")
        return 0
    

    def edit_note(self, note, color):
        note_data = []
        try:
            with open('notes.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=',')
                rows = list(reader)
                for row in rows:
                    if row['note_id'] == self.note_id:
                        row['note'] = note
                        row['color'] = color
                    note_data.append(row)
            with open('notes.csv', 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['note_id', 'user_id', 'note', 'color'])
                writer.writeheader()
                writer.writerows(note_data)
            self.ids.note.text = ""
            self.ids.color.text = ""
            self.note_id = ""
            self.edit = False
            self.show_popup("Success", "Piezīme rediģēta")
            self.manager.current = 'main'
        except Exception as e:
            self.show_popup("Error", f"Error: {str(e)}")
        



    def show_popup(self, title, message):
        layout = BoxLayout(orientation='vertical', padding=10)
        label = Label(text=message)
        button = Button(text='OK', size_hint=(1, 0.25))
        layout.add_widget(label)
        layout.add_widget(button)
        popup = Popup(title=title, content=layout, size_hint=(0.75, 0.5))
        button.bind(on_release=popup.dismiss)
        popup.open()

    def delete_note(self):
        try:
            note_data = []
            with open('notes.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=',')
                for row in reader:
                    if row['note_id'] != self.note_id:
                        note_data.append(row)
            with open('notes.csv', 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['note_id', 'user_id', 'note', 'color'])
                writer.writeheader()
                writer.writerows(note_data)
            self.ids.note.text = ""
            self.ids.color.text = ""
            self.note_id = ""
            self.edit = False
            self.show_popup("Success", "Piezīme dzēsta")
            self.manager.current = 'main'
        except Exception as e:
            self.show_popup("Error", f"Error: {str(e)}")



    def logout_button(self):
        self.current_user = ""
        self.welcome_text = "Welcome!"
        self.manager.current = 'login'
