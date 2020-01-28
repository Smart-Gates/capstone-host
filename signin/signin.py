from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
import time

import requests
import json
import weather
from capstone_requests import *
import sqlite3

Builder.load_file("/home/pi/repos/capstone-host/signin/signin.kv")

class SigninWindow(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_interval(self.update_wicon, 180)
        Clock.schedule_interval(self.update_wtemp, 180)
        
    # Login Functionality
    def validate_user(self):
        
        # Sign-in post request 
        req = Reqs()
        req.set_ext("/api/auth/signin")

        # User/Email, Password and Error ids from signin.kv
        user = self.ids.usr_field
        pwd  = self.ids.pwd_field
        error = self.ids.error
        
        # text components 
        uname = user.text
        pswd  = pwd.text
        
        # make login request
        payload = {'email': uname, 'password': pswd}
        headers = {'Content-type' : 'application/json'}        
        req.post_req(req.get_url(), payload, headers)

        if req.get_status() == 200:
            if req.get_role() == "USER":
                self.parent.parent.current = 'scrn_rem'
            else:
                self.parent.parent.current = 'scrn_ad'
        if uname == '' or pswd == '':
            error.text = '[color=#FF0000]username and password required[/color]'
            
    # returns current time
    def update_time(self, *args):
        tim = self.ids.cur_time
        tim.text = time.asctime()
        return time.asctime()
    
    # returns weather icon
    def update_wicon(self, *args):
        return weather.get_icon(weather.new_weather_req())
    
    # returns curremt temp
    def update_wtemp(self, *args):
        return weather.get_temp(weather.new_weather_req())
    
class SignApp(App):
    def build(self):
        return SigninWindow()
    
if __name__=="__main__":
    sa = SignApp()
    sa.run()
    