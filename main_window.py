from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

import csv
import os
import ast


class MainWindow(Screen):
    current_user = StringProperty("")
    welcome_text = StringProperty("Sveiks!")
    id = StringProperty("")

    def update_welcome_text(self):
        self.welcome_text = f"Sveiks, {self.current_user}!"

    def display_notes(self, notes_list):
        self.ids.notes.clear_widgets()
        for note in notes_list:
            print(note)
            note_label = Label(
            text=note['note'],
            size_hint_y=None,
            height=40,
            color=(note['color']))
            with note_label.canvas.before:
                Color(0.2, 0.4, 0.8, 1) 
                Rectangle(pos=note_label.pos, size=note_label.size)
            note_label.bind(pos=self.update_rect, size=self.update_rect)
            
            self.ids.notes.add_widget(note_label)


    def update_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.2, 0.4, 0.8, 1)  # Background color
            Rectangle(pos=instance.pos, size=instance.size)
                
    def new_note(self):
        note_editor = self.manager.get_screen('note_editor')
        note_editor.user_id = self.id

        self.manager.current = 'note_editor'


    def logout_button(self):
        self.current_user = ""
        self.welcome_text = "Welcome!"
        self.manager.current = 'login'

    def on_enter(self):
        self.display_notes(self.get_notes())

    def get_notes(self):
        notes_list = []
        try:
            if os.path.exists('notes.csv'):
                with open('notes.csv', 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter=',')
                    for row in reader:
                        if row['user_id'] == self.id:
                            note = {
                                'note': row['note'],
                                'color': row['color']
                            }
                            notes_list.append(note)
            
        except Exception as e:
            print(f"Error: {e}")

        return notes_list



        