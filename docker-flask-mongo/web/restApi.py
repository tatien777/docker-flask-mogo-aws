"""
Registration of a user 0 tokens
Each user gets 10 tokens
Store a sentence on our database for 1 token
Retrieve his stored sentence on out database for 1 token
"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import time
import redis
import bcrypt 
# db
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

clients = MongoClient("mongodb://db:27017")
db = clients.SentencesDatabase
users = db["Users"]

class Register(Resource):
    def post(self):
        # Step1 is to get posted data by the user
        postedData = request.get_json()
        
        # Get the data
        username = postedData["username"]
        password = postedData["password"]
        
        #hash(password + salt) = wdftdad4
        
    

"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import time
import redis
# db
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

clients = MongoClient("mongodb://db:27017")
db = clients.aNewDB
UserNum = db["UserNum"]

UserNum.insert({
    'num_of_users': 0
})


def get_hit_count():
    retries = 5
    while True:
        try:
            return "error"
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


def checkData(postData, functionName):
    if(functionName == "add" or functionName == "subtract" or functionName == "multiply"):
        if "x" not in postData or "y" not in postData:
            return 301
        else:
            return 200
    elif (functionName == "divide"):
        if "x" not in postData or "y" not in postData:
            return 301
        elif postData['y'] == 0:
            return 302
        else:
            return 200


class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update({}, {"$set": {"num_of_users": new_num}})
        return str("Hello user " + str(new_num))


class Add(Resource):

    def post(self):
       # the rosource using method POST for create some news
        # Step 1: Get posted data
        postedData = request.get_json()
        # step 1b: veify validity of posted data
        status_code = checkData(postedData, "add")
        if (status_code != 200):
            retJson = {
                "Message": "An error of variable input ",
                "status_code":  status_code
            }
            return jsonify(retJson)
        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)

        # Step2 : added the posted data
        ret = x + y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class Subtract(Resource):

    def post(self):
       # the rosource using method POST for create some news
        # Step 1: Get posted data
        postedData = request.get_json()
        # step 1b: veify validity of posted data
        status_code = checkData(postedData, "subtract")
        if (status_code != 200):
            retJson = {
                "Message": "An error of parameter ",
                "status_code":  status_code
            }
            return jsonify(retJson)
        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)

        # Step2 : subtract the posted data
        ret = x - y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)


class Multiply(Resource):
    def post(self):
           # the rosource using method POST for create some news
        # Step 1: Get posted data
        postedData = request.get_json()
        # step 1b: veify validity of posted data
        status_code = checkData(postedData, "multiply")
        if (status_code != 200):
            retJson = {
                "Message": "An error of parameter ",
                "status_code":  status_code
            }
            return jsonify(retJson)
        x = postedData['x']
        y = postedData['y']
        z = postedData['z']
        x = int(x)
        y = int(y)

        # Step2 : multiply the posted data
        ret = x * y * z
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)


class Divide(Resource):
    def post(self):
           # the rosource using method POST for create some news
        # Step 1: Get posted data
        postedData = request.get_json()
        # step 1b: veify validity of posted data
        status_code = checkData(postedData, "divide")
        if (status_code != 200):
            retJson = {
                "Message": "An error of parameter ",
                "status_code":  status_code
            }
            return jsonify(retJson)
        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)

        # Step2 : divide the posted data
        ret = x / y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)


api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/divide")
api.add_resource(Visit, "/hello")


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

"""