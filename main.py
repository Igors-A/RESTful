from flask import Flask
from flask_restful import Resource, Api
import requests
#test client by Igors Anastasjevs
app = Flask(__name__)
api = Api(app)
@app.route("/")
def jsontest():
    jsn = requests.get('http://127.0.0.1:5000/sent/Counter-Strike').json()
    return jsn
if __name__ == '__main__':
    app.run(debug=True, port=6268)