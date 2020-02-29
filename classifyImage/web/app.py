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
        