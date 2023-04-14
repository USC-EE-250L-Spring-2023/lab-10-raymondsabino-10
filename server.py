from flask import Flask, request, jsonify
import numpy as np

from main import process1, process2


app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome'})

# TODO: Create a flask app with two routes, one for each function.
# The route should get the data from the request, call the function, and return the result.

@app.route('/offloadprocess1', methods=['GET','POST'])
def offloadprocess1():
    data = request.get_json() #Retrieve data
    res = jsonify(process1(data["data"])) #Execute process1 on data, put into json form
    res.status_code = 200 #Status code for ok
    return res

@app.route('/offloadprocess2', methods=['GET','POST'])
def offloadprocess2():
    data = request.get_json() #Retrieve data
    res = jsonify(process2(data["data"])) #Execute process1 on data, put into json form
    res.status_code = 200 #Status code for ok
    return res

if __name__ == '__main__':
    print('Starting server')
    app.run(port=5000, debug=True)