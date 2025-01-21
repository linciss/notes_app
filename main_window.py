from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

import csv
import os
import ast


class MainWindow(Screen):
    current_user = StringProperty("")
    welcome_text = StringProperty("Sveiks!")
    id = StringProperty("")

    def update_welcome_text(self):
        self.welcome_text = f"Sveiks, {self.current_user}!"

    def filter_notes(self):
        self.ids.notes.clear_widgets()
        notes_list = self.get_notes()
        notes_list = sorted(notes_list, key=lambda x: x['title'])
        print(notes_list)
        self.display_notes(notes_list)



    def display_notes(self, notes_list):
        self.ids.notes.clear_widgets()
        for note in notes_list:
            note_layout = FloatLayout(size_hint_y=None, height=40)
            
            note_label = Label(
                text=note['title'],
                size_hint=(1, None), 
                height=40,
                text_size=(self.width, None),
                color=(1, 1, 1, 1),
                pos_hint={"x": 0, "y": 0},
                halign='left',
                )
            

            note_label.bind(size=lambda widget, size: setattr(widget, 'text_size', (size[0], None)))

            note_label.bind(pos=lambda instance, value, note_color=note['color']: self.update_rect(instance, value, note_color))

            note_label.bind(size=lambda instance, value, note_color=note['color']: self.update_rect(instance, value, note_color))

            note_label.bind(on_touch_down=lambda instance, touch, note_text=note['note']: self.on_note_click(instance, touch, note_text))

            delete_button = Button(text='Dzēst', size_hint=(None, None), size=(60, 30), pos_hint={"right": 0.98, "y": 0.12}, background_color=(1, 0, 0, 1))
            delete_button.bind(on_release=lambda btn, note_id=note['id']: self.delete_note(note_id))

            edit_button = Button(text='Rediģēt', size_hint=(None, None), size=(60, 30), pos_hint={"right": 0.8, "y": 0.12},background_color=(0, 1, 0, 1))
            edit_button.bind(on_release=lambda btn, title=note['note'], note_id=note['id'], note_color=note['color'], note_category=note['category'], note_title=note['title']: self.edit_note(title,note_id, note_color, note_category, note_title))

            note_layout.add_widget(note_label)
            note_layout.add_widget(edit_button)
            note_layout.add_widget(delete_button)

            self.ids.notes.add_widget(note_layout)
            
    def delete_note(self, note_id):
            try:
                note_data = []
                with open('notes.csv', 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter=',')
                    for row in reader:
                        if row['note_id'] != note_id:
                            note_data.append(row)
                with open('notes.csv', 'w', encoding='utf-8', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=['note_id', 'user_id', 'note', 'color', 'category'])
                    writer.writeheader()
                    writer.writerows(note_data)
                self.display_notes(self.get_notes())
            except Exception as e:
                self.show_popup("Error", f"Error: {str(e)}")
    def hex_to_rgba(self, hex):
        hex = hex.lstrip('#')
        return tuple(int(hex[i:i+2], 16) / 255 for i in (0, 2, 4)) + (1.0,)
    
    def edit_note(self, title, note_id, note_color, note_category, note_title):
        note_editor = self.manager.get_screen('note_editor')
        note_editor.user_id = self.id
        note_editor.note_id = note_id
        note_editor.ids.note_title.text = note_title
        note_editor.edit = True
        note_editor.ids.note.text = title
        note_editor.color.text = note_color
        note_editor.ids.category_btn.text = note_category
        self.manager.current = 'note_editor'

    def on_note_click(self, instance, touch, note_text):
            if instance.collide_point(*touch.pos):
                note_preview = self.manager.get_screen('note_preview')
                note_preview.note.text = note_text
                note_preview.note_title.text = instance.text
               
                self.manager.current = 'note_preview'


    def rgba_to_hex(self, rgba):
        return '#{:02x}{:02x}{:02x}'.format(
            int(rgba[0] * 255),
            int(rgba[1] * 255),
            int(rgba[2] * 255),
        )

    def update_rect(self, instance, value, note_color):
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


    def enter_settings(self):
        settings_screen = self.manager.get_screen('settings')
        settings_screen.current_user = self.current_user
        settings_screen.ids.username.text = self.current_user
        self.manager.current = 'settings'

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
                                'id': row['note_id'],
                                'category': row['category'],
                                'title': row['title']
                            }
                            notes_list.append(note)
            
        except Exception as e:
            print(f"Error: {e}")

        return notes_list



        