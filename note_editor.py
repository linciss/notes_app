from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty
import os
import csv

class NoteEditor(Screen):
    user_id = StringProperty("")
    note = ObjectProperty(None)
    color = ObjectProperty(None)
    # catgeory = ObjectProperty(None)


    def create_note(self):
        note = self.ids.note.text
        color = self.ids.color.text
        if(color == ""):
            color = "#FFFFFF"
        
        if len(color) != 7 or color[0] != "#":
            self.show_popup("Error", "Please enter a valid color in hex format")
            return
        
        print(color)
        try:
            if note:
                with open('notes.csv', 'a', encoding='utf-8', newline='') as file:
                    file.write(f"{self.get_row_count()},{self.user_id},{note},{color}\n")
                self.ids.note.text = ""
                self.ids.color.text = ""
                self.manager.current = 'main'
            else:
                self.show_popup("Error", "Please enter a note")
        except Exception as e:
            self.show_popup("Error", f"Failed to create note: {str(e)}")


    def get_row_count(self):
        try:
            if os.path.exists('notes.csv'):
                with open('notes.csv', 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    row_count = sum(1 for row in reader)
                    print(row_count)
                    return row_count
        except Exception as e:
            self.show_popup("Error", f"Failed to get row count: {str(e)}")
        return 0

    def logout_button(self):
        self.current_user = ""
        self.welcome_text = "Welcome!"
        self.manager.current = 'login'
