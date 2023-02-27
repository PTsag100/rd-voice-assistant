from flask import *
import json

app=Flask(__name__)

@app.route('/',methods=['GET'])
def home_page():
    user_query=str(request.args.get('user'))
    data=request.json
    print(data)
    data_set={'Page':'Home','Message':"Loaded home page"+user_query}
    return data


if __name__=='__main__':
    app.run(port=5000)
