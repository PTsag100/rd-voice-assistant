import random
import json
import pickle
import numpy as np
import nltk
from flask import *
from flask_cors import CORS
# nltk.download()

from nltk.stem import WordNetLemmatizer
import tensorflow as tf

lemmatizer=WordNetLemmatizer()
intents=json.loads(open('intents2.json').read())

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
    ERROR_THRESHOLD=0.20
    results=[[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD] # get the most matching answers

    results.sort(key=lambda x:x[1],reverse=True) # take always the first answer which means the most maching
    return_list=[]
    for r in results:
        return_list.append({'intent':classes[r[0]],'probability':str(r[1])}) # show the probability of each class based on the input
    return return_list

def get_response(intents_list,intents_json):
    tag=intents_list[0]['intent']
    list_of_intents=intents_json['intents']
    for i in list_of_intents:
        if i['tag']==tag:
            result=random.choice(i['responses'])
            break
    return result

print('RD is running')

# while True:
#     message=input("")
#     message=message.lower()
#     ints=predict_class(message)
#     res=get_response(ints,intents)
#     print(res)


app=Flask(__name__)
CORS(app)

@app.route('/',methods=['POST'])
def home_page():
    # user_query=str(request.args.get('user')) this is a qeuery
    message_data=request.json
    if message_data is not None:
        print(message_data["message"])
        message=message_data["message"]
        message=message.lower()
        ints=predict_class(message)
        res=get_response(ints,intents)
        # res.headers.add('Access-Control-Allow-Origin', '*')
        return res
    else:
        return None

@app.route('/',methods=['GET'])
def page():
    # user_query=str(request.args.get('user')) this is a qeuery
    return "Hello"

if __name__=='__main__':
    app.run(port=5000)
