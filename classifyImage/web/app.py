from flask import Flask,jsonify,request
from flask_restful import Api,Resource
from pymongo import MongoClient
import bcrypt
import requests
import subprocess
import json

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")

db = client.ImageRecognition
users = db["Users"]


def userExist(username):
    if users.find({"Username":username}).count() == 0:
        return False
    else:
        return True
    
class Register(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]
        password = postedData["password"]
        
        if userExist(username):
            retJson = {
                "status":301,
                "msg": "Invalid Username"
            }
        hashed_pw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())    
        
        users.insert({
            "Username":username,
            "Password": hashed_pw,
            "Tokens":5
        })
        
        retJson = {
            "status":200,
            "msg": "You successfullly signed up API for CI"
        }
        return jsonify(retJson)
def verifyPw(username,pw):
    if not userExist(username): return False
    hashed_pw = users.find({"Username":username})[0]["Password"]
    
    if bcrypt.hashpw(pw.encode('utf8'),hashed_pw) == hashed_pw:
        return True
    else: return False
    
def generateReturnDict(status,msg):
    retJson = {
        "status":status,
        "msg":msg
    }
    return jsonify(retJson)

def verifyCrredentials(username,pw):
    if not userExist(username):
        return generateReturnDict(301,"Invalid Username"), True
    correct_pw = verifyPw(username,pw)
    if not correct_pw:
        return generateReturnDict(302,"invalid Password"), True
    
class Classify(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]
        password = postedData["password"]
        url  =     postedData["url"]
        
        retJson,error = verifyCrredentials(username,password)
        if error:
            return jsonify(retJson)
        
        tokens = users.find({
            "Username":username
        })[0]["Tokens"]
        
        if tokens <=0:
            return jsonify(generateReturnDict(303,"Not enough tokens"))
        r = requests.get(url)
        
        retJson = {}
        with open("temp.jpg","wb") as f:
            f.write(r.content)
            proc = subprocess.Popen('python imageClassify.py --model_dir =. --image_file=./temp.jpg')
            proc.communicate()[0]
            proc.wait()
            with open("text.txt") as g:
                retJson = json.load(g)
        users.update({"Username":username},{'$set':{"Tokens": tokens -1}})
        return jsonify(retJson)        

class Refill(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]
        password = postedData["admin_pw"]
        amount = postedData["amount"]
        
        if not userExist(username):
            return generateReturnDict(301,"Invalid Username")
        correnct_pw = "abc123"
        
        if not password == correnct_pw:
            return generateReturnDict(304,"Invalid Admin pw")
        
        users.update({
            "Username":username
        },{
            "$set":{
                "Tokens":amount
            }
        })
        return generateReturnDict(200,"Refilled successfully")
    
api.add_resource(Register,'/register')
api.add_resource(Classify,'/classify')
api.add_resource(Refill,'/refill')

if __name__ == "__main___":
    app.run(host='0.0.0.0')