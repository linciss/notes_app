from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
import os
import csv
import re

class NoteEditor(Screen):
    user_id = StringProperty("")
    note = ObjectProperty(None)
    note_title = ObjectProperty(None)
    color = ObjectProperty(None)
    edit = False
    note_id = StringProperty("")
    category = StringProperty("Izvēlies kategoriju")


    def create_note(self):
        title = self.ids.note_title.text
        note = self.ids.note.text
        color = self.ids.color.text

        if note == "":
            self.show_popup("Error", "Ievadi tekstu")
            return
        if title == "":
            self.show_popup("Error", "Ievadi nosaukumu")
            return  
    
        if(color == ""):
            color = "#FFFFFF"
        
        if len(color) != 7 or color[0] != "#":
            self.show_popup("Error", "Ievadi hex kodu ar # zīmi priekšā vai pārbaudi vai ir 7 simboli") 
            return
        
        category = self.ids.category_btn.text

        if category == "Izvēlies kategoriju":
            self.show_popup("Error", "Lūdzu izvēlies kategoriju")
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
                    file.write(f"{self.get_row_count()},{self.user_id},{title},{note},{color},{category}\n")
                self.ids.note.text = ""
                self.ids.color.text = ""
                self.show_popup("Success", "Piezīme pievienota")
                self.go_back()
            else:
                self.show_popup("Error", "Ievadi tekstu")
        except Exception as e:
            self.show_popup("Error", f"Error: {str(e)}")
            


    def go_back(self): 
        self.edit = False
        self.ids.category_btn.text = "Izvēlies kategoriju"
        self.manager.current = 'main'
        self.note = ""
        self.note_title = ""

       
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
                        row['title'] = self.ids.note_title.text
                        row['note'] = note
                        row['color'] = color
                        row['category'] = self.ids.category_btn.text
                    note_data.append(row)
            with open('notes.csv', 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['note_id', 'user_id', 'title', 'note', 'color', 'category'])
                writer.writeheader()
                writer.writerows(note_data)
            self.ids.note.text = ""
            self.ids.color.text = ""
            
            self.note_id = ""
            self.show_popup("Success", "Piezīme rediģēta")
            self.go_back()
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
