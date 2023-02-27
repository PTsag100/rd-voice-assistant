import sys
import threading
import tkinter
import speech_recognition
import pyttsx3
import json


file=open("intents.json")
data=json.load(file)
print(data)

class Assistant:
    def __init__(self):
        self.recognizer=speech_recognition.Recognizer()

        self.speaker=pyttsx3.init()
        self.speaker.setProperty("rate",150)
        
        self.root=tkinter.Tk()
        self.label=tkinter.Label(text="O",font=("Arial",120,"bold"))
        self.label.pack()

    def create_file(self):
        with open("testfile.txt","w") as f:
            f.write("Test was succesfull")

    def getResponse(text):
        print(data)
        return "hello"

    def run_assistant(self):
        while True:
            try:
                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic,duration=0.2)
                    audio=self.recognizer.listen(mic) 
                    text=self.recognizer.recognize_google(audio)
                    text=text.lower()

                    if "hey rd" in text:
                        audio=self.recognizer.listen(mic)
                        text=self.recognizer.recognize_google(audio)
                        text=text.lower()
                        if text=="stop":
                            self.speaker.say("Bye")
                            self.speaker.runAndWait()
                            self.speaker.stop()
                            self.root.destroy()
                            sys.exit(0)
                        else:
                            if text is not None:
                                response=self.getResponse(text)
                                if response is not None:
                                    self.speaker.say(response)
                                    self.speaker.runAndWait()


            except:
                print('there was an error')
                sys.exit(0)
                continue




Assistant()
