import random
import json
import pickle
import numpy as np
import nltk
from flask import *
from flask_cors import CORS
import functionalities
import subprocess
import webbrowser
import os
import pyautogui
import sys
import math
import speedtest

from nltk.stem import WordNetLemmatizer
import tensorflow as tf
front_end_path=os.path.join(os.path.dirname(__file__),'../rd-front-end')
print(front_end_path)
p=subprocess.Popen(["python","-m","http.server","8000"], cwd=front_end_path)
webbrowser.open("http://localhost:8000")
lemmatizer=WordNetLemmatizer()
intents=json.loads(open('intents.json').read())

words=pickle.load(open('words.pkl','rb'))
classes=pickle.load(open('classes.pkl','rb'))
model=tf.keras.models.load_model('chatbotmodel.h5')

def clean_up_senetence(sentence):
    sentence_words=nltk.word_tokenize(sentence)
    sentence_words=[lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words=clean_up_senetence(sentence)
    bag=[0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word ==w:
                bag[i]=1
    return np.array(bag)


def predict_class(sentence):
    bow=bag_of_words(sentence)
    res=model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD=0.18
    results=[[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD] # get the most matching answers
    results.sort(key=lambda x:x[1],reverse=True) # take always the first answer which means the most maching
    print(sentence)
    print(results)
    if results[0][0]==17 and sentence[0]!='h':
        return "unknown"
    return_list=[]
    for r in results:
        return_list.append({'intent':classes[r[0]],'probability':str(r[1])}) # show the probability of each class based on the input
    return return_list

def get_response(intents_list,intents_json):
    tag=intents_list[0]['intent']
    list_of_intents=intents_json['intents']
    for i in list_of_intents:
        if i['tag']==tag:
            result=i['responses']
            break
    return result

print('RD is running')

def bytes_to_mb(size_bytes):
    i=int(math.floor(math.log(size_bytes,1024)))
    power=math.pow(1024,i)
    size=round(size_bytes/power,2)
    return size



app=Flask(__name__)
CORS(app)

@app.route('/',methods=['GET'])
def test():
    return None

@app.route('/',methods=['POST'])
def main_page():
    # user_query=str(request.args.get('user')) this is a qeuery
    stop=False
    if stop:
        sys.exit(0)
    
    message_data=request.json
    if message_data is not None:
        print(message_data["message"])
        message=message_data["message"]
        message=message.lower()
        ints=predict_class(message)
        if(ints=="unknown"):
            return [""]
        res=get_response(ints,intents)
        response_data=[]

        #the first is the response of the voice assistant
        response_data.append(res[0])

        # all the other are the functions that calls
        if(len(res)>1):
            for r in res[1:]:
                response_data.append(eval(r))
        return response_data
    else:
        return None

@app.route('/changetodo',methods=['POST'])
def todo():
    with open('todo.json', 'w') as openfile:
        json.dump(request.json,openfile)
    return "success"

@app.route('/internet',methods=['GET'])
def internet():
    wifi=speedtest.Speedtest()
    print('Getting download speed')
    download_speed=wifi.download()
    print('Getting upload speed')
    upload_speed=wifi.upload()
    download_speed=bytes_to_mb(download_speed)
    upload_speed=bytes_to_mb(upload_speed)
    upload_speed=round(upload_speed/1000,2)
    return [download_speed,upload_speed]

if __name__=='__main__':
    app.run(port=5000)
