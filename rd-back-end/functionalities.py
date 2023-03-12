import requests
import geocoder
import subprocess
import webbrowser
import pyautogui
import datetime
import json

sub=None

def weather():
    api_key="YOUR API KEY"
    myloc = geocoder.ip('me')
    myloc=myloc.json
    response=requests.get("http://api.openweathermap.org/geo/1.0/direct?q={}&appid={}".format(myloc['city'],api_key))
    lat=response.json()[0]['lat']
    lon=response.json()[0]['lon']
    response=requests.get("https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(lat,lon,api_key))
    data=[]
    data.append({'type':"weather"})
    data.append(response.json()['name'])
    data.append(response.json()['weather'][0]['icon'])
    data.append(response.json()['weather'][0]['description'])
    data.append(response.json()['main']['temp'])
    data.append(response.json()['main']['humidity'])
    data.append(response.json()['wind']['speed'])
    print(data)
    return data

def closePanel():
   return [{ "type": "close" }]

def openControl():
    global sub
    sub = subprocess.Popen('python Virtual_Mouse.py')

def stopControl():
    sub.kill()

def Search(sentence):
    tempText=sentence.split()
    if any('search' in word for word in tempText):
        tempText.remove("search")

    if any('for' in word for word in tempText):
        tempText.remove("for")
    speakText=' '.join(tempText)
    searchLink='+'.join(tempText)    
    webbrowser.open("https://www.google.com/search?q={}&oq={}".format(searchLink,searchLink))
    return [{ "type": "speak" },"Searching for {}".format(speakText)]

def Typing(sentence):
    tempText=sentence.split()
    if any('type' in word for word in tempText):
        tempText.remove("type")

    if any('write' in word for word in tempText):
        tempText.remove("write")
    speakText=' '.join(tempText)
    pyautogui.write(speakText)
    return [{ "type": "speak" },"Typing {}".format(speakText)]

def Backspace(sentence):
    tempText=sentence.split()
    if any('word' in word for word in tempText):
        pyautogui.hotkey('ctrl','backspace')

    else:
        pyautogui.press('backspace')

def time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    return [{ "type": "time" },current_time]

def date():
    today = datetime.date.today()
    current_date = today.strftime("%B %d, %Y")
    return [{ "type": "date" },current_date]

def getTodos():
    with open('todo.json', 'r') as openfile:
        json_object = json.load(openfile)
    return [{ "type": "todo" },json_object]