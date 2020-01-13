from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
import time

import requests
import sqlite3

Builder.load_file("signin/signin.kv")

class SigninWindow(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_time, 1)
    
    # Login Functionality
    def validate_user(self):
        
        # Connect to database
        conn = sqlite3.connect('Desktop/Kivy/ver0.2/signin/Smart_Gates_DB.db')
        c = conn.cursor()
        
        # User/Email, Password and Error ids from signin.kv
        user = self.ids.usr_field
        pwd  = self.ids.pwd_field
        error = self.ids.error
        
        # text components 
        uname = user.text
        pswd  = pwd.text
        
        # Login checking
        find_user = ("SELECT * FROM employees WHERE first_name = ? AND pass = ?")
        c.execute(find_user, [(uname), (pswd)])
        results = c.fetchall()
        
        if uname == '' or pswd == '':
            self.parent.parent.current = 'scrn_rem'
            #error.text = '[color=#FF0000]username and password required[/color]'
        #else:
            
            
    
    # returns current time
    def update_time(self, *args):
        tim = self.ids.cur_time
        tim.text = time.asctime()
        return time.asctime()
        
class SignApp(App):
    def build(self):
        return SigninWindow()
    
if __name__=="__main__":
    sa = SignApp()
    sa.run()
    
    
    