from flask import Flask,request,jsonify
from flask_pymongo import pymongo
import text2emotion as te
import db
import json
#test to insert data to the data base
import datetime
import openai

app = Flask(__name__)




x = datetime.datetime.now()

print(x.year)
print(x.month)


@app.route('/openai',methods=['POST'])
def openaiapi():

    openai.api_key = "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"

    input = request.json
    input = input["input"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":input}]
    )
    resp ={
        "response":response.choices[0].message.content
    }
    return resp

@app.route("/login",methods=["GET","POST"])
def log():
    dict = request.json
    # print(dict['name'])
    st = dict['Name']
    ct = db.db.MP_UserLogin.find({"Name":st})
    if(ct!=None):
        print("Found")
    else:
        print("Not Found")
    c=0
    for i in ct:
        print(i)
        c=c+1

    if(c!=0):
        return "Success",200
    else:
        return "Failed"

    
@app.route("/getjournals",methods=["GET","POST"])
def journals():
    dict = request.json
    # print(dict['name'])
    st = dict['Name']
    print(st)
    ct = db.db.Journal.find({"Name":st})
    print(ct)
    l = []
    dt = {}
    ch = 0
    cs = 0
    cf = 0
    ca = 0
    csur = 0
    for i in ct:
        if(i['Notes']=='uffp'):
            print(i['Date'])
        if(i['Mood'].lower()=="happy"):
            ch += 1
        elif(i['Mood'].lower()=="sad"):
            cs += 1
        elif(i['Mood'].lower()=="fear"):
            cf += 1
        elif(i['Mood'].lower()=="angry"):
            ca += 1
        elif(i['Mood'].lower()=="surprise"):
            csur += 1
        
        
        i['YY']=i['Date'].year
        i['MM']=i['Date'].month
        i['DD']=i['Date'].day
        dt['Notes']=i['Notes']
        dt['YY']=i['YY']
        dt['MM']=i['MM']
        dt['DD']=i['DD']
        dt['Mood']=i['Mood']
        ret = json.dumps(dt)
        print(ret)
        l.append(ret)

    current = {}
    if(ch>=cs and ch >= cf and ch>= csur and ch>=ca):
        current['Currently'] = "happy"
    elif(cs>ch):
        current['Currently'] = "sad"
    elif(csur>ch):
        current['Currently'] = "surprise"
    elif(ca>ch):
        current['Currently'] = "angry"
    elif(cf>ch):
        current['Currently'] = "fear"

    current['Notes'] = "Sad"
    current['YY'] = "Sad"
    current['DD'] = "Sad"
    current['MM'] = "Sad"
    current['Mood'] = "Sad"
    sendback = json.dumps(current)
    l.append(sendback)


    if(len(l)>0):
        print('Backedn')
        print(l)
        return l
    else:
        return "Not Found"
    return l

    

@app.route("/newuser", methods=["POST"])
def newuser():
    
    dict = request.json
    # print()

    dict = {"Name":dict['Name']}
    
    ct = db.db.MP_UserLogin.find({"Name":dict['Name']})
    if(ct!=None):
        print("Found")
    else:
        print("Not Found")
    c=0
    for i in ct:
        print(i)
        c=c+1
    
    if(c==0):
        db.db.MP_UserLogin.insert_one(dict)
        return dict['Name']+" Created",200
    else:
        return "User Exists"
    
    return "error",404

    
    

@app.route("/test",methods=["post","get"])
def test():

    dict = request.json
    emotion = te.get_emotion(dict['Notes'])
    Keymax = max(zip(emotion.values(), emotion.keys()))[1]
    print(Keymax)
    dict['Mood'] = Keymax
    dict['Date'] = datetime.datetime.now()
    db.db.Journal.insert_one(dict)
    return "success"

@app.route("/notes",methods=["get"])
def notes():

    # db.db.Journal.insert_one(dict)
    items = db.db.Journal.find({'notes': 'mmm'})
    for i in items:
        print(i)
    # return items
    return list(db.db.Journal.find({},{"_id":0}))

    # for x in col.find({}, {"_id":0, "coursename": 1, "price": 1 }):
        

@app.route('/')
def index():
    return "Hello, world!"

if __name__ == '__main__':
    app.run(debug=True)