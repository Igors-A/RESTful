#done by Igors Annastasjevs, fy18ia


import random
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import sqlite3, json

app = Flask(__name__)#set ups Flask-based server
api = Api(app)
con = sqlite3.connect('sources/steam1.db', check_same_thread=False)#connects to database
cur = con.cursor()
cur.execute("SELECT * FROM games LIMIT 1")
top = cur.fetchall()[0]#get keys for json/dictionary in order to sort information about the game from steam1.db
#steam1.db was created from steam.csv, which can be openly received from https://www.kaggle.com/nikdavis/steam-store-games?select=steam.csv
#steam1.db was slightly modified adding with appr. 5 games
def fromtupletodicofdb(t):#function which basically explaining creates dictionary from tuple
    thegame = {}
    for i in range(len(top) - 7):#columms from 12 to 18 were excess
        thegame.update({top[i]: t[i]})
    return thegame
class Agame():#a game class, its "legacy" class as it was repurposed from storing 1 game into storing 1 game and 3 recommendations
    def __init__(self,game):
        cur.execute("SELECT * FROM games WHERE column2="+"\'"+game+"\'")#searches a game
        out = cur.fetchall()
        thegame = fromtupletodicofdb(out[0])
        genres = thegame['genres'].split(';')#for recommendation getting
        #коммент ниже можно удалить
        """this was added because one of the games had this tag. The game, which names I tested, had 1% of 'Sexual Content',
        but it was enough for sqlite to present a lot of possibly pornographic games"""
        #command generation
        if 'Sexual Content' in genres:
            genres.remove('Sexual Content')
        command = "SELECT * FROM games WHERE (column10 LIKE \'%"+genres[0]+"%\'"
        if(len(genres)>1):
            for i in range(1,len(genres)):
                command += " OR \'%" + genres[i] + "%\'"
        command += ") AND ( NOT column2="+"\'"+game+"\')"
        cur.execute(command)
        #receiving data
        out = cur.fetchall()
        arr = []
        #random recommentations from array
        for i in range(0,3):
            j = random.randint(0, len(out))
            arr.append(fromtupletodicofdb(out[j]))
        getout = {
            "the game": thegame,#the game receive from client
            "recomm": arr#array of recommended games
        }
        self.jsn = json.dumps(getout)#sents 'json'
class Sender(Resource):
    def get(self, game):
        self.a = Agame(game)#getting data
        return self.a.jsn#sending data
api.add_resource(Sender, '/sent/<game>')
if __name__ == '__main__':
    app.run(debug=True)#ports could be changed here in case of