from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.popup import Popup
import time
from capstone_requests import * 
from Smart_Gates_Database import *
from RFID_RW import *

Builder.load_file("/home/pi/repos/capstone-host/admin/admin.kv")

class NewUser(FloatLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add(self):
        
        # text input 
        first    = self.ids.first
        last     = self.ids.last
        email    = self.ids.email
        password = self.ids.password
        
        # create new org user request
        new_user = Create_Org_User()
        new_user.post_req(new_user.get_url(), new_user.create_payload(email.text, password.text, first.text, last.text), Reqs.get_headers_auth())
        print(new_user.get_status())
        
class RemUser(FloatLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def remove(self):
        
        # text input
        email = self.ids.email

        # get the id using the user email
        req_find_id = Get_All_Org_Users()
        req_find_id.get_req(req_find_id.get_url(), req_find_id.create_payload(), Reqs.get_headers_auth())
        id = req_find_id.get_id_from_email(email.text)

        # remove user request
        remove_user = Delete_Org_User(id)
        remove_user.del_req(remove_user.get_url(), remove_user.create_payload(), Reqs.get_headers_auth())
        
        print(remove_user.get_status())
        
class AssignRFID(FloatLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def assign_three_steps(self):

        # text input 
        email = self.ids.email

        # get the id using the user email
        req_find_id = Get_All_Org_Users()
        req_find_id.get_req(req_find_id.get_url(), req_find_id.create_payload(), Reqs.get_headers_auth())
        id = req_find_id.get_id_from_email(email.text)

        # generate tag
        access_database = Smart_Gates_Database()
        access_database.create_user_table()
        tag = access_database.generate_tag()
        
        # write tag to RFID Card
        writer = RFID_RW()
        writer.write_RFID(tag)

        # add id and tag to local database
        access_database.add_new_user(id, tag)

        # request to add tag to server database
        req_assign = Set_RFID_Req()
        req_assign.post_req(req_assign.get_url(), req_assign.create_payload(tag, id), Reqs.get_headers_auth())
        print(req_assign.get_text())

class AdminWindow(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def add_user(self):
        show = NewUser()
        popWin = Popup(title = "New User", content = show, size_hint = (0.5, 0.5))
        show.ids.cancel.on_release = popWin.dismiss
        popWin.open()
    
    def rem_user(self):
        show = RemUser()
        popWin = Popup(title = "Remove User", content = show, size_hint = (0.5, 0.5))
        show.ids.cancel.on_release = popWin.dismiss
        popWin.open()
        
    def assign_RFID(self):
        show = AssignRFID()
        popWin = Popup(title = "Assign RFID", content = show, size_hint = (0.5, 0.5))
        show.ids.cancel.on_release = popWin.dismiss
        popWin.open()
    
    def rem_screen(self):
        self.parent.parent.current = 'scrn_rem'
        
    def logout(self):
        self.parent.parent.current = 'scrn_si'
        
class AdminApp(App):
    def build(self):
        return AdminWindow()
    
if __name__=="__main__":
    ad = AdminApp()
    ad.run()