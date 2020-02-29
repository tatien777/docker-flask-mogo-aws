from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy


app = Flask(__name__)
api = Api(app)

clients = MongoClient("mongodb://db:27017")

db = clients.SimilarityDB
users = db["Users"]


def UserExist(username):
    if users.find({"Username": username}).count() == 0:
        return False
    else:
        return True


class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        if UserExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonify(retJson)
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
            'Username': username,
            "Password": hashed_pw,
            "Tokens": 6
        })

        retJson = {
            "status": 200,
            "msg": "You've successfully singed up the API",
            "hashed_pw": str(hashed_pw),
            "name": str(username)
        }
        return jsonify(retJson)


def verifyPw(username, pw):
    if not UserExist(username):
        return False
    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(pw.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


def countTokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]
    return tokens


class Detect(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData['username']
        password = postedData['password']
        text1 = postedData["text1"]
        text2 = postedData["text2"]

        if not UserExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonify(retJson)

        correct_pw = verifyPw(username, password)
        print(correct_pw)
        if not correct_pw:
            retJson = {
                "status": 301,
                "msg": "Invalid Password"
            }
        num_tokens = countTokens(username)

        if num_tokens <= 0:
            retJson = {
                "status": 303,
                "msg": "Your're out of tokens, plz refill",
                "num_tokens": num_tokens
            }
            return jsonify(retJson)
        # Calculate the edit distance
        # nlp = spacy.load('en_core_web_sm')

        # text1 = nlp(text1)
        # text2 = nlp(text2)

        # # Ratio is a number bw 0 and 1 the closer to 1, the more similar text 1
        # # and text2 are
        # ratio = text1.similarity(text2)

        retJson = {
            "status": 200,
            # "similarity": ratio,
            "msg": "Similarity score calculated successfully"
        }

        current_tokens = countTokens(username)
        query_user = {"Username": username}
        value_update = {"$set": {"Tokens": current_tokens - 1}}
        users.update({"Username": username}, value_update)
        print(jsonify(retJson))
        return jsonify(retJson)
class Refill(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        refill_amount = postedData["refill"]

        if not UserExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid username"
            }
            return jsonify(retJson)

        correct_pw = "abc123"
        if not password == correct_pw:
            retJson = {
                "status": 304,
                "msg": "Invalid Admin Password"
            }
            return jsonify(retJson)
        current_tokens = countTokens(username)
        query_user = {"Username": username}
        value_update = {'$set': {"Tokens": refill_amount}}
        users.update( {"Username": username},
                     value_update)

        retJson = {
            "status": 200,
            "msg": "Refilled successfully"
        }
        return jsonify(retJson)


api.add_resource(Register, '/register')
api.add_resource(Detect, '/detect')
api.add_resource(Refill, '/refill')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
