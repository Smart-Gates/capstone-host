from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.popup import Popup

import datetime
import time
from utils.userdata import UserData
from capstone_requests import *
from Smart_Gates_Database import *

import socket
import time

Builder.load_file("/home/pi/repos/capstone-host/reminders/reminders.kv")

# list of lists to list
def flatten_list(lst_list):
    data = []
    for sublist in lst_list:
        for item in sublist:
            data.append(item)
    return data

# check internet connection
def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

## Reminder Popup Window
class NewRemPop(FloatLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def minimumdate(self):
        d = datetime.datetime.now()
        return time.mktime(d.timetuple())

    def maximumdate(self):
        d = datetime.datetime.now() + datetime.timedelta(hours=1)
        return time.mktime(d.timetuple())

    def timestamp_to_datetime(self, timestamp):
        return datetime.datetime.fromtimestamp(
            int(timestamp)
        ).strftime('%Y-%m-%dT%H:%M:%S')
    
    def new_rem(self):
        title = self.ids.title
        descr = self.ids.descrip
        slider = self.ids.slider
        
        addReminder = Create_Reminder_Req()
        addReminder.post_req(addReminder.get_url(), addReminder.create_payload(title.text, descr.text, self.timestamp_to_datetime(slider.value)), Reqs.get_headers_auth())

## Event Popup Window
class NewEvePop(FloatLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def minimumdate(self):
        d = datetime.datetime.now()
        return time.mktime(d.timetuple())

    def maximumdate(self):
        d = datetime.datetime.now() + datetime.timedelta(hours=1)
        return time.mktime(d.timetuple())

    def timestamp_to_datetime(self, timestamp):
        return datetime.datetime.fromtimestamp(
            int(timestamp)
        ).strftime('%Y-%m-%dT%H:%M:%S')
    
    def new_eve(self):
        title = self.ids.title
        descr = self.ids.descrip
        member = self.ids.member
        slider = self.ids.slider
        
        addEvent = Create_Events_Req()
        addEvent.post_req(addEvent.get_url(), addEvent.create_payload(title.text, descr.text, '350 victoria St', self.timestamp_to_datetime(slider.value), '2020-03-28T08:00:00', [member.text]), Reqs.get_headers_auth())
        print(addEvent.get_status)
        
## Reminder Window
class ReminderWindow(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # login test
##        req = Signin_Req()
##        req.post_req(req.get_url(), req.create_payload('john@email.com', 'password'), Reqs.get_headers_noauth())
##        self.load_info()
        
    def load_info(self):
        if is_connected():
            
            # get all reminders
            req2 = Get_Reminders_Req()
            req2.get_req(req2.get_url(), req2.create_payload(), Reqs.get_headers_auth())
            
            # reminders screen
            content = self.ids.reminders
            userd = UserData(data =req2.get_rem_info(), num = req2.get_rem_count(), flag = 0)
            content.add_widget(userd)
            
            # get all events
            req3 = Get_Events_Req()
            req3.get_req(req3.get_url(), req3.create_payload(), Reqs.get_headers_auth())
  
            # meetings screen
            content2 = self.ids.meetings
            userm = UserData(data = req3.get_event_info(), num = req3.get_event_count(), flag = 1)
            content2.add_widget(userm)
        
        else:
            
            access_database = Smart_Gates_Database()
            
            rem = access_database.get_reminders()
            eve = access_database.get_events()
            
            rem = flatten_list(rem)
            eve = flatten_list(eve)
            
            # reminders screen
            content = self.ids.reminders
            userd = UserData(data = rem, num = int(len(rem)/5), flag = 0)
            content.add_widget(userd)
            
            # meetings screen
            content2 = self.ids.meetings
            userm = UserData(data = eve, num = int(len(eve)/7), flag = 1)
            content2.add_widget(userm)
            
        
    def change_screen(self, instance):
        if instance.text == 'View Reminders':
            self.ids.scrn_mngr.current = 'reminders'
        elif instance.text == 'View Meetings':
            self.ids.scrn_mngr.current = 'meetings'
            
    def add_rem_pop(self):
        show = NewRemPop()
        popWin = Popup(title = "New Reminder", content = show, size_hint = (0.5, 0.5))
        show.ids.cancel.on_release = popWin.dismiss
        show.ids.addrem.on_release = self.load_info
        popWin.open()
    
    def add_eve_pop(self):
        show = NewEvePop()
        popWin = Popup(title = "New Event", content = show, size_hint = (0.5, 0.5))
        show.ids.cancel.on_release = popWin.dismiss
        show.ids.addrem.on_release = self.load_info
        popWin.open()

    def logout(self):
        
        if is_connected():
            self.parent.parent.current = 'scrn_si'
            
            # save reminders and events to database
            access_database = Smart_Gates_Database()
            
            req3 = Get_Events_Req()
            req3.get_req(req3.get_url(), req3.create_payload(), Reqs.get_headers_auth())
            
            # get 
            data = req3.get_event_info()
            num = req3.get_event_count()
            
            # commit changes to event table
            access_database.create_events_table()
            access_database.create_event(data, num)
            
            # get all reminders
            req2 = Get_Reminders_Req()
            req2.get_req(req2.get_url(), req2.create_payload(), Reqs.get_headers_auth())
            
            data2 = req2.get_rem_info()
            num2  = req2.get_rem_count()
            
            # commit changes to reminder table
            access_database.create_reminders_table()
            access_database.create_reminder(data2, num2)
            
            
        else:
            self.parent.parent.current = 'scrn_si'
            
class ReminderApp(App):
    def build(self):
        return ReminderWindow()
        
if __name__=="__main__":
    re = ReminderApp()
    re.run()
