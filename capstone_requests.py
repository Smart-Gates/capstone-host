import requests
import json
import hashlib

class Reqs:
    
    # static variable for access token
    token = "Empty"
    
    def __init__(self, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        self._ext = ""
        self._url = url
        self._req = req
       
    # set extension for the base url    
    def set_ext(self, ext):
        self._ext = ext
    
    # get full url    
    def get_url(self):
        return self._url + self._ext

    # returns the status of the request    
    def get_status(self):
        return self._req.status_code

    # returns the text of the request
    def get_text(self):
        return self._req.json()

    # post request (default)
    def post_req(self, url, payload, headers):
        self._req = requests.post(url, data =json.dumps(payload),  headers = headers)

    # get request (default)
    def get_req(self, url, payload, headers):
        self._req = requests.get(url, data =json.dumps(payload),  headers = headers)

    # put request (default)
    def put_req(self, url, payload, headers):
        self._req = requests.put(url, data =json.dumps(payload),  headers = headers)

    # delete request (default)
    def del_req(self, url, payload, headers):
        self._req = requests.delete(url, data =json.dumps(payload),  headers = headers)

    # static method to get headers (default, no authentication)
    @staticmethod
    def get_headers_noauth():
        return {'Content-type' : 'application/json'}

    # static method to get headers (default, with authentication)
    @staticmethod
    def get_headers_auth():
        return {'Content-type' : 'application/json', 'Authorization' : 'Bearer ' + Reqs.get_cur_token()}   

    # static method to return the access token
    @staticmethod
    def get_cur_token():
        return Reqs.token

     # static method to destroy the access token
    @staticmethod
    def des_cur_token():
        Reqs.token = "Empty"

class Signup_Req(Reqs):

    def __init__(self, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/auth/signup"

    # create sign-up payload
    def create_payload(self, first, last, email, password):
        return { 'firstName': first, 'lastName': last, 'email': email, 'password': password }


class Signin_Req(Reqs):
    
    def __init__(self, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/auth/signin"

    # create sign-in payload
    def create_payload(self, email, password):
        return {"email": email, "password": password}

    # post request (sign-in)
    def post_req(self, url, payload, headers):
        self._req = requests.post(url, data =json.dumps(payload),  headers = headers)
        Reqs.token = self._req.json()["accessToken"]
       
    # returns the access token
    def get_token(self):
        return self._req.json()["accessToken"]

    # returns the role of the user
    def get_role(self):
        return self._req.json()["user"]["roles"][0]["authority"]

class Current_User_Info(Reqs):

    def __init__(self, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/auth/user"

    # create user info payload
    def create_payload(self):
        return {}

class Create_Org_User(Reqs):

    def __init__(self, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/organizations/Device_1/users"

    # create create-user payload
    def create_payload(self, email, password, first, last):
        return { 'email': email, 'password': password, 'firstName': first, 'lastName': last }

class Delete_Org_User(Reqs):

    def __init__(self, id, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/organizations/Device_1/users/" + str(id)
        
    # create delete-user payload
    def create_payload(self):
        return {}

class Get_All_Org_Users(Reqs):

    def __init__(self, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/organizations/Device_1/users"

    # create delete-user payload
    def create_payload(self):
        return {}

    # returns number of paramaeters in request
    def get_param_count(self):
        return len(self.get_text()["_embedded"]["userList"])

    # returns id of a given email
    def get_id_from_email(self, email):
        id = []
        for x in range(self.get_param_count()):
            if email == self.get_text()["_embedded"]["userList"][x]['email']:
                id = self.get_text()["_embedded"]["userList"][x]['id']
        return id

class Get_Events_Req(Reqs):

    def __init__(self, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/events"

    # create get-events payload
    def create_payload(self):
        return {}

    # returns the number of events
    def get_event_count(self):
        try:
            return len(self.get_text()["_embedded"]["eventList"])
        except KeyError:
            return 0
        
    # returns all event info
    def get_event_info(self):
        table = []
        for x in range(self.get_event_count()):
            try:
                table.append(self.get_text()["_embedded"]["eventList"][x]['id'])
                table.append(self.get_text()["_embedded"]["eventList"][x]['title'])
                table.append(self.get_text()["_embedded"]["eventList"][x]['description'])
                table.append(self.get_text()["_embedded"]["eventList"][x]['start_time'])
                table.append(self.get_text()["_embedded"]["eventList"][x]['end_time'])
                table.append(self.get_text()["_embedded"]["eventList"][x]['creator']['id'])
                try:
                    table.append(self.get_text()["_embedded"]["eventList"][x]['attendees'][0]['id'])
                except IndexError:
                    table.append(0)
            except KeyError:
                pass
        return table
    
class Create_Events_Req(Reqs):
    
    def __init__(self, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/events"

    # create create-event payload
    def create_payload(self, title, description, location, start_time, end_time, attendee_email):
        return {'title': title, 'description': description, 'location': location, 'start_time': start_time, 'end_time': end_time, 'attendee_email' : attendee_email}

class Update_Event_Req(Reqs):
    
    def __init__(self, eventID, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/events/" + eventID

    # create update-event payload
    def create_payload(self, title, description, location, start_time, end_time, attendee_email):
        return {'title': title, 'description': description, 'location': location, 'start_time': start_time, 'end_time': end_time, 'attendee_email' : attendee_email}

class Delete_Event_Req(Reqs):
    
    def __init__(self, eventID, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/events/" + eventID

    # create delete-event payload
    def create_payload(self):
        return {}

class Create_Reminder_Req(Reqs):
    
    def __init__(self, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/reminders"

    # create create-reminder payload
    def create_payload(self, title, description, start_time):
        return {'title': title, 'description': description, 'start_time': start_time}

class Update_Reminder_Req(Reqs):
   
    def __init__(self, reminderID, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/reminders/" + reminderID

    # create update-reminder payload
    def create_payload(self, title, description, start_time):
        return {'title': title, 'description': description, 'start_time': start_time}

class Get_Reminders_Req(Reqs):
    
    def __init__(self, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/reminders"

    # create get-reminders payload
    def create_payload(self):
        return {}

    # returns the number of reminders
    def get_rem_count(self):
        try:
            return len(self.get_text()["_embedded"]["reminderList"])
        except KeyError:
            return 0
    
    # returns all reminder info
    def get_rem_info(self):
        table = []
        for x in range(self.get_rem_count()):
            try:
                table.append(self.get_text()["_embedded"]["reminderList"][x]['id'])
                table.append(self.get_text()["_embedded"]["reminderList"][x]['title'])
                table.append(self.get_text()["_embedded"]["reminderList"][x]['description'])
                table.append(self.get_text()["_embedded"]["reminderList"][x]['start_time'])
                table.append(self.get_text()["_embedded"]["reminderList"][x]['creator']['id'])
            except KeyError:
                pass
        return table

class Delete_Reminder_Req(Reqs):
    
    def __init__(self, reminderID, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/reminders/" + reminderID

    # create delete-reminder payload
    def create_payload(self):
        return {}

class Send_Image_Req(Reqs):
    
    def __init__(self, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/notification/image"

    # create send-image payload
    def create_payload(self, title, message, email, imageData):
        return {'title': title, 'message': message, 'topic':"", 'email': email, 'imageData': imageData}

class Set_RFID_Req(Reqs):
    
    def __init__(self, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/rfid"
    
    # create set RFID payload
    def create_payload(self, tag, userID):
        hashed_tag = hashlib.pbkdf2_hmac('sha256', tag.encode(), b'SmartGates', 100)
        return {'tag': hashed_tag.hex(), 'userId': userID}

class RFID_Signin_Req(Reqs):

    def __init__(self, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/rfid/signin"
    
    # post request (sign-in)
    def post_req(self, url, payload, headers):
        self._req = requests.post(url, data =json.dumps(payload),  headers = headers)
        Reqs.token = self._req.json()["accessToken"]
    
    # create RFID sign in payload
    def create_payload(self, tag):
        hashed_tag = hashlib.pbkdf2_hmac('sha256', tag.encode(), b'SmartGates', 100)
        return {'tag': hashed_tag.hex()}

    # returns the role of the user
    def get_role(self):
        return self._req.json()["user"]["roles"][0]["authority"]
    
class Get_RFID_List_Req(Reqs):
    
    def __init__(self, url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com", req = ""):
        super().__init__(url, req)
        self._ext = "/api/rfid/users"

    # create get RFID list payload
    def create_payload(self):
        return {}



## testing        
##req = Signin_Req()
##req.post_req(req.get_url(), req.create_payload('rami@email.com', 'password'), Reqs.get_headers_noauth())

#req3 = Create_Org_User()
#req3.post_req(req3.get_url(), req3.create_payload("test@email.com", "password", "Rami", "Saad"), Reqs.get_headers_auth())
#print(req3.get_status())

#req2 = Get_All_Org_Users()
#req2.get_req(req2.get_url(), req2.create_payload(), Reqs.get_headers_auth())

#print(req2.get_id_from_email("rami@email.com"))

##req2 = Get_Reminders_Req()
##req2.get_req(req2.get_url(), req2.create_payload(), Reqs.get_headers_auth())
##
##print(req2.get_text())

#print(req.get_status())
#print(Reqs.get_cur_token())
#print(Signin_Req.token)
#print(Reqs.token)

