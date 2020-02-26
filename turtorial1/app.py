from flask import Flask,jsonify,request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return """<b>  Hello world </b>
<h> new thing </h>
"""
@app.route('/hi')
def hi_everyone():
    # c = 1/0
    json_ex = {
        'field1':'abc',
        'field2':'def'
    }
    h = print('New page')
    h
    return jsonify(json_ex)

@app.route('/add_two_nums',methods=["POST"])
def add_2_nums():
    # get x,y from the posted data
    dataDict = request.get_json()
    if "y" not in dataDict:
        return "ERROR",305
    x = dataDict["x"]
    y = dataDict["y"]
    
    # Add z = x + y
    z = x + y
    #Prepare a JSon,"z":z
    retJSON = {
        "z" : z
    }
    #return jsonify(map_prepared)
    return jsonify(retJSON), 200
if __name__ == "__main__":
    app.run(host="127.0.0.1",port=80)
    
