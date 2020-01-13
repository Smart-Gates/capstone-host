from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import time

Builder.load_file("admin/admin.kv")

class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class AdminApp(App):
    def build(self):
        return AdminWindow()
    
if __name__=="__main__":
    ad = AdminApp()
    ad.run()