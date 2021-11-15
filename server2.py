from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import sqlite3, json
app = Flask(__name__)
api = Api(app)
con = sqlite3.connect('sources/steam1.db', check_same_thread=False)
cur = con.cursor()
cur.execute("SELECT * FROM games LIMIT 1")
top = cur.fetchall()[0]
#print(top)
class Agame():
    def __init__(self,game):
        #print(type(game))
        cur.execute("SELECT * FROM games WHERE column2="+"\'"+game+"\'")
        arr = cur.fetchall()[0]
        x = {}
        for i in range(len(top)-7):
            x.update({top[i]:arr[i]})
        self.jsn = json.dumps(x)
#a = Agame('Counter-Strike')
#print(a.jsn)
class Sender(Resource):
    def get(self, game):
        self.a = Agame(game)
        #print(self.a.jsn)
        return self.a.jsn
api.add_resource(Sender, '/sent/<game>')
if __name__ == '__main__':
    app.run(debug=True)