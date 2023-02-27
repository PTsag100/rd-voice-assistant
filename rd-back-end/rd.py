
import speech_recognition as sr 
import pyttsx3
import json
import webbrowser
import subprocess
import sys
import PySimpleGUI as sg
from multiprocessing import process

layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]
window = sg.Window("Demo", layout)

sub=None

file=open("intents.json")
data=json.loads(file.read())
print(data)
file.close()



def Speak(text):
    engine.say(text)
    engine.runAndWait()


def Search(text):
    tempText=text.split()
    if any('search' in word for word in tempText):
        tempText.remove("search")

    if any('for' in word for word in tempText):
        tempText.remove("for")
    speakText=' '.join(tempText)
    searchLink='+'.join(tempText)    
    webbrowser.open("https://www.google.com/search?q={}&oq={}".format(searchLink,searchLink))
    Speak("Searching for "+speakText)

    

def openControl():
    global sub
    print('starting')
    sub = subprocess.Popen('python Virtual_Mouse.py')
    Speak("Starting manual control")

def stopControl():
    print("ending")
    sub.kill()
    Speak('Stoping manual control')


def gui():
    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            break

    window.close()
   

gui()

engine=pyttsx3.init()
recognizer=sr.Recognizer()



while True:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source,duration=0.2)
        print("recording")
        recordedaudio=recognizer.listen(source,timeout=100)
        try:
            text=recognizer.recognize_google(recordedaudio)
            text=text.lower()
            if text is not None:
                for request in data:
                    if request in text:
                        responses=data[request].split(";")
                        print(responses)
                        for response in responses:
                            eval(response)
                        break
                    

        except Exception as ex:
            print("error")
            recognizer=sr.Recognizer()
            continue

