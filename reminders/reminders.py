from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
#from capstone_requests import *

from utils.userdata import UserData
import time
from capstone_requests import *

Builder.load_file("/home/pi/repos/capstone-host/reminders/reminders.kv")

class ReminderWindow(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # login test
        req = Reqs()
        req.set_ext("/api/auth/signin")
        payload = {'email': 'john@email.com', 'password': 'password'}
        headers = {'Content-type' : 'application/json'}        
        req.post_req(req.get_url(), payload, headers)
        
        # get all reminders
        req2 = Reqs()
        req2.set_ext("/api/reminders")
        payload2 = {}
        headers2 = {'Authorization' : 'Bearer ' + Reqs.get_cur_token()}
        req2.get_req(req2.get_url(), payload2, headers2)
        
        # reminders screen
        content = self.ids.reminders
        userd = UserData(data = req2.get_rem_info(), num = req2.get_rem_count(), flag = 0)
        content.add_widget(userd)
        
        req3 = Reqs()
        req3.set_ext("/api/events")
        payload3 = {}
        headers3 = {'Authorization' : 'Bearer ' + Reqs.get_cur_token()}
        req3.get_req(req3.get_url(), payload3, headers3)
        
        # meetings screen
        content2 = self.ids.meetings
        userm = UserData(data = req3.get_event_info(), num = req3.get_event_count(), flag = 1)
        content2.add_widget(userm)
        
        
    def change_screen(self, instance):
        if instance.text == 'View Reminders':
            self.ids.scrn_mngr.current = 'reminders'
        elif instance.text == 'View Meetings':
            self.ids.scrn_mngr.current = 'meetings'
        
class ReminderApp(App):
    def build(self):
        return ReminderWindow()
    
if __name__=="__main__":
    re = ReminderApp()
    re.run()
