from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.clock import Clock

from capstone_requests import *
from RFID_RW import *
from Smart_Gates_Database import *

import time
import requests
import json
import weather
import sqlite3
import socket
import base64
import os

Builder.load_file("/home/pi/repos/capstone-host/signin/signin.kv")

# check internet connection
def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

## Guest Photo Notfication Popup Window
class GuestPhoto(FloatLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def create_req(self):
        
        # get the text input
        title   = self.ids.title
        message = self.ids.message
        email   = self.ids.email
        
        # send the requests
        image_req = Send_Image_Req()
        image_req.post_req(image_req.get_url(), image_req.create_payload(title.text, message.text, email.text, b64_string.decode('utf-8')), Reqs.get_headers_noauth())
        print(image_req.get_text())

class SigninWindow(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.detect_card, 1)
        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_interval(self.update_wicon, 180)
        Clock.schedule_interval(self.update_wtemp, 180)

    # call all the functions that need to be scheduled for the sign in screen       
    def schedule(self):
        Clock.schedule_interval(self.detect_card, 1)
        Clock.schedule_interval(self.update_time, 60)
        Clock.schedule_interval(self.update_wicon, 180)
        Clock.schedule_interval(self.update_wtemp, 180)
        
    # suspends all the sign in screen functions before switching screens 
    def suspend(self):
        Clock.unschedule(self.detect_card)
        Clock.unschedule(self.update_time)
        Clock.unschedule(self.update_wicon)
        Clock.unschedule(self.update_wtemp)
                    
    # Login Functionality
    def validate_user(self):
        if is_connected():
            # User/Email, Password and Error ids from signin.kv
            user = self.ids.usr_field
            pwd  = self.ids.pwd_field
            error = self.ids.error
            
            # text components 
            uname = user.text
            pswd  = pwd.text
            
            # Sign-in post request
            req = Signin_Req()
            req.post_req(req.get_url(), req.create_payload(uname, pswd), Reqs.get_headers_noauth())

            if req.get_status() == 200:
                self.ids.usr_field.text = ''
                self.ids.pwd_field.text = ''
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
        if is_connected():
            return weather.get_icon(weather.new_weather_req())
            #pass
        
    # returns curremt temp
    def update_wtemp(self, *args):
        if is_connected():
            #return "Offline mode"
            return weather.get_temp(weather.new_weather_req())
        else:
            return "Offline mode"
    
    def capture(self):
        
        # take the photo and save it
        camera = self.ids.camera
        camera.export_to_png("notification.png")
    
        # get the base64 encoding
        with open("notification.png", "rb") as img_file:
            global b64_string
            b64_string = base64.b64encode(img_file.read())
        
        # delete the image file
        os.remove("notification.png")
        
        # pop-up information
        show = GuestPhoto()
        popWin = Popup(title = "Guest Photo Notification", content = show, size_hint = (0.5, 0.5))
        show.ids.cancel.on_release = popWin.dismiss
        popWin.open()
        
    def detect_card(self, *args):
        
        # read RFID card
        test = RFID_RW()
        tag = test.read_RFID()
        print(tag)
        
        # internet connection case
        if is_connected():
            
            # login test
            req = Signin_Req()
            req.post_req(req.get_url(), req.create_payload('john@email.com', 'password'), Reqs.get_headers_noauth())
            
            ##
            if tag is not None and len(tag) == 64:
                login_RFID = RFID_Signin_Req()
                login_RFID.post_req(login_RFID.get_url(), login_RFID.create_payload(tag), Reqs.get_headers_noauth())
                if login_RFID.get_status() == 200:
                    if login_RFID.get_role() == "USER":
                        self.parent.parent.current = 'scrn_rem'
                    else:
                        self.parent.parent.current = 'scrn_ad'
        
        # no internet connection case
        else:
            if tag is not None:
                access_database = Smart_Gates_Database()
                if access_database.login_RFID(tag) > 0:
                    self.parent.parent.current = 'scrn_rem'
                    
class SignApp(App):
    def build(self):
        return SigninWindow()
    
if __name__=="__main__":
    sa = SignApp()
    sa.run()
    