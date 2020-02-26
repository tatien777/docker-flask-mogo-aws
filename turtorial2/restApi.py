from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


def checkData(postData, functionName):
    if(functionName == "add" or functionName == "subtract" or functionName == "multiply" ):
        if "x" not in postData or "y" not in postData:
            return 301
        else:
            return 200
    elif (functionName == "divide"):
        if "x" not in postData or "y" not in postData:
            return 301
        elif postData['y']==0:
            return 302 
        else:
            return 200 
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
        x = int(x)
        y = int(y)
        
        # Step2 : multiply the posted data
        ret = x * y
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


@app.route('/')
def hello():
    return "hello wordld"


if __name__ == "__main__":
    app.run(debug=True)
