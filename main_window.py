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
            note_label = Label(
            text=note['note'],
            size_hint_y=None,
            height=40,
            color=(1,1,1,1))

            note_label.bind(pos=lambda instance, value, note_color=note['color']: self.update_rect(instance, value, note_color))
            note_label.bind(size=lambda instance, value, note_color=note['color']: self.update_rect(instance, value, note_color))

            note_label.bind(on_touch_down=lambda instance, touch, note_id=note['id'], note_color=note['color']: self.on_note_click(instance, touch, note_id, note_color))

            self.ids.notes.add_widget(note_label)

    def hex_to_rgba(self, hex):
        hex = hex.lstrip('#')
        return tuple(int(hex[i:i+2], 16) / 255 for i in (0, 2, 4)) + (1.0,)
    

    def on_note_click(self, instance, touch, note_id, note_color):
        if instance.collide_point(*touch.pos):
            note_editor = self.manager.get_screen('note_editor')


            note_editor.user_id = self.id
            note_editor.note.text = instance.text
            note_editor.edit = True
            note_editor.note_id = note_id

            note_editor.color.text = note_color


            self.manager.current = 'note_editor'

    def rgba_to_hex(self, rgba):
        return '#{:02x}{:02x}{:02x}'.format(
            int(rgba[0] * 255),
            int(rgba[1] * 255),
            int(rgba[2] * 255),
        )

    def update_rect(self, instance, value, note_color):
        print(note_color)
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*self.hex_to_rgba(note_color))
            Rectangle(pos=instance.pos, size=instance.size)
                
    def new_note(self):
        note_editor = self.manager.get_screen('note_editor')
        note_editor.user_id = self.id

        self.manager.current = 'note_editor'


    def logout_button(self):
        self.current_user = ""
        self.welcome_text = "Sveiks!"
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
                                'color': row['color'],
                                'id': row['note_id']
                            }
                            notes_list.append(note)
            
        except Exception as e:
            print(f"Error: {e}")

        return notes_list



        