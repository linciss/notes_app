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

class NotePreview(Screen):
    note = ObjectProperty(None)
    note_title = ObjectProperty(None)



    def go_back(self): 
        self.note.text = ""
        self.note_title.text = ""
        self.manager.current = 'main'
    


    def on_open(self):
        self.ids.note.text = self.note
        self.ids.note_title.text = self.note_title

        



    def show_popup(self, title, message):
        layout = BoxLayout(orientation='vertical', padding=10)
        label = Label(text=message)
        button = Button(text='OK', size_hint=(1, 0.25))
        layout.add_widget(label)
        layout.add_widget(button)
        popup = Popup(title=title, content=layout, size_hint=(0.75, 0.5))
        button.bind(on_release=popup.dismiss)
        popup.open()

