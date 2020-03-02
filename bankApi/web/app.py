from flask import Flask,jsonify,request
from flask_restful import Api,Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.BankApi
users = db["Users"]


def checkUser(username):
    if users.find({"Username": username}).count() ==0:
        return False
    else: return True
def generateJson(status,msg):
    retJson = {
        "status": status,
        "msg" : msg
    }
    return retJson

class Register(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]
        password = postedData["password"]
        
        if checkUser(username):
            return jsonify(generateJson(301,"Invalid Username"))
        
        hashed_pw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
        
        users.insert({
            "Username":username,
            "Password": hashed_pw,
            "Own":0,
            "Debt":0
        })
        
        return  jsonify(generateJson(200,"Successfully signed up Bank API"))

def verifyPw(username,pw):
    if not checkUser(username):return False
    hashed_pw = users.find({
        "Username":username
    })[0]["Password"]
    
    if bcrypt.hashpw(pw.encode('utf8'),hashed_pw) == hashed_pw:
        return True
    else:
        return False

def cashWithUser(username):
    cash = users.find({
        "Username":username
    })[0]["Own"]
    return cash
def debtWithUser(username):
    debt = users.find({
        "Username":username
    })[0]["Debt"]
    return debt

## ErrorDictionary , True/False
def verifyCredentials(username,pw):
    if not checkUser(username): 
        return generateJson(301,"Invalid Username"),True
    
    correct_pw = verifyPw(username,pw)
    if not correct_pw:
        return generateJson(302,"Incorrect Password"),True
    return None,False

def updateAcount(username,balance,method="Own"):
    if method!= "Own" and method!= "Debt":
        return jsonify(generateJson(302,"Incorrect method"))
    users.update({
             "Username":username
         },{
             '$set':{
                 method: balance
             }
         })
        
class Add(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]        
        password = postedData["password"]
        money = postedData["amount"]
        
        retJson,error = verifyCredentials(username,password)
        
        if error:
            return jsonify(retJson)
        if money <= 0:
            return jsonify(generateJson(304,"wrong input: amount must be >= 0"))
        cash = cashWithUser(username)
        money -= 1
        bank_cash = cashWithUser("BANK")
        updateAcount("BANK",bank_cash+1)
        updateAcount(username,cash+money)
        
        return jsonify(generateJson(200,"the money entered the account"))
    
class Transfer(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]
        password = postedData["password"]
        to = postedData["to"]
        money = postedData["amount"]
        
        retJson,error = verifyCredentials(username,password)
        
        if error : 
            return jsonify(retJson)
        
        cash = cashWithUser(username)
        if cash<= 0:
            return jsonify(generateJson(304,"You're out of money, please add or take a loan"))
        
        if not checkUser(to):
            return jsonify(generateJson(301,"Invalid Username"))
        cash_from = cashWithUser(username)
        cash_to = cashWithUser(to)
        bank_cash = cashWithUser("BANK")
        
        updateAcount("BANK",bank_cash+1)
        updateAcount(to,cash_to+money-1)
        updateAcount(username,cash_from - money)
        
        return jsonify(generateJson(200,"Amount transferred successfully"))
    
class Balance(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]
        password = postedData["password"]
        
        retJson,error = verifyCredentials(username,password)
        
        if error:
            return jsonify(retJson)
        
        retJson = users.find({
            "Username":username
        },{
            "Password":0,
            "_id":0
        })[0]
        print(retJson)

        return jsonify(retJson)

class TakeLoan(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]
        
        retJson,error = verifyCredentials(username,password)
        
        if error:
            return jsonify(retJson)
        
        cash = cashWithUser(username)
        debt = debtWithUser(username)
        updateAcount(username,cash+money)
        updateAcount(username,debt+money,method="Debt")
        
        return jsonify(generateJson(200,"loan added to your account"))
class PayLoan(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]
        
        retJson,error = verifyCredentials(username,password)
        
        if error:
            return jsonify(retJson)
        
        cash = cashWithUser(username)
        
        if cash < money: 
            return(jsonify(generateJson(303,"Not enough cash in your account")))
        
        
        debt = debtWithUser(username)
        if money > 0 and money <= debt:
            return(jsonify(generateJson(304,"Invalid Money ")))
        
        updateAcount(username,cash - money)
        updateAcount(username,debt - money,method="Debt")
        
        return(jsonify(200,"You're successfully paid your loan"))
    
api.add_resource(Register,'/register')
api.add_resource(Add,'/add')
api.add_resource(Transfer,'/transfer')
api.add_resource(Balance,'/balance')
api.add_resource(TakeLoan,'/takeloan')
api.add_resource(PayLoan,'/payloan')

if __name__ == "__main__":
    app.run(host='0.0.0.0')

        
        
    