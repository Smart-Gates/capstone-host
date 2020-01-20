from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import time

Builder.load_file("/home/pi/repos/capstone-host/reminders/reminders.kv")

class ReminderWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ReminderApp(App):
    def build(self):
        return ReminderWindow()
    
if __name__=="__main__":
    re = ReminderApp()
    re.run()