from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from signin.signin import SigninWindow
from reminders.reminders import ReminderWindow
from admin.admin import AdminWindow

class MainWindow(BoxLayout):
    
    signin_widget = SigninWindow()
    reminders_widget = ReminderWindow()
    admin_widget = AdminWindow()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_rem.add_widget(self.reminders_widget)
        self.ids.scrn_ad.add_widget(self.admin_widget)
        
class MainApp(App):
    def build(self):
        return MainWindow()
    
if __name__=="__main__":
    MainApp().run()