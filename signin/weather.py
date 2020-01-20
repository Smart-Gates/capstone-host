import requests
import json

url = "https://api.openweathermap.org/data/2.5/weather?q=Toronto&apikey=838466457358f67cc04ded0ec4c9e7ea"
r = 1
payload = {}
headers = {'Content-type' : 'application/json'}

def new_weather_req():
    return requests.get(url, data =json.dumps(payload),  headers = headers).json()

def get_status(req):
    return req["cod"]

def get_temp(req):
    return (str(round(req["main"]["temp"] - 273.15, 1)) + "\u00b0" + "C") 
    
def get_icon(req):
    return ("weather/" + req["weather"][0]["icon"] + ".png")


