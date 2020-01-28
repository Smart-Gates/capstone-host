import requests
import json

class Reqs:
    
    # static variable for access token
    token = "Empty"
    
    def __init__(self, ext = ""):
        self._ext = ext
        self._url = "http://capstonespringboot-env.zegtxprh2h.us-east-2.elasticbeanstalk.com" 
        self._req = ""
        self._payload = ""
        self._headers = ""
        
    # set extension for the base url    
    def set_ext(self, ext):
        self._ext = ext
        
    # set payload for the request
    def set_payload(self, payload):
        self._payload = payload
        
    # set headers for the request
    def set_headers(self, headers):
        self._headers = headers
    
    # get full url    
    def get_url(self):
        return self._url + self._ext

    # post request
    def post_req(self, url, payload, headers):
        self._req = requests.post(url, data =json.dumps(payload),  headers = headers)
        # set token if login request
        if self._ext == "/api/auth/signin":
            Reqs.token = self._req.json()["accessToken"]
    
    #get request
    def get_req(self, url, payload, headers):
        self._req = requests.get(url, data =json.dumps(payload),  headers = headers)
        
    
    # returns the status of the request    
    def get_status(self):
        return self._req.status_code
    
    # returns the text of the request
    def get_text(self):
        return self._req.json()
    
    # returns the acces token
    def get_token(self):
        return self._req.json()["accessToken"]
    
    # returns the role of the user
    def get_role(self):
        return self._req.json()["user"]["roles"][0]["authority"]
    
    # static method to return access token
    @staticmethod
    def get_cur_token():
        return Reqs.token

## make their own subclasses later for better maintainabillity
    
    # returns the number of reminders
    def get_rem_count(self):
        return len(self.get_text()["_embedded"]["reminderList"])
    
    # returns all reminder info
    def get_rem_info(self):
        table = []
        for x in range(self.get_rem_count()):
            table.append(self.get_text()["_embedded"]["reminderList"][x]['title'])
            table.append(self.get_text()["_embedded"]["reminderList"][x]['description'])
            table.append(self.get_text()["_embedded"]["reminderList"][x]['start_time'])
        return table
    
    # returns the number of events
    def get_event_count(self):
        return len(self.get_text()["_embedded"]["eventList"])
        
    # returns all event info
    def get_event_info(self):
        table = []
        for x in range(self.get_event_count()):
            table.append(self.get_text()["_embedded"]["eventList"][x]['title'])
            table.append(self.get_text()["_embedded"]["eventList"][x]['description'])
            table.append(self.get_text()["_embedded"]["eventList"][x]['start_time'])
            table.append(self.get_text()["_embedded"]["eventList"][x]['end_time'])
        return table
    
############################################# testing 
#payload = {'email': 'john@email.com', 'password': 'password'}
#headers = {'Content-type' : 'application/json'}

#req = Reqs()

#req.set_ext("/api/auth/signin")
#req.post_req(req.get_url(), payload, headers)

#payload2 = {}
#headers2 = {'Authorization' : 'Bearer ' + Reqs.get_cur_token()}

#req2 = Reqs()

#req2.set_ext("/api/reminders")
#req2.get_req(req2.get_url(), payload2, headers2)

#print(req.get_role())

#full_url = url + ext

#print(full_url)