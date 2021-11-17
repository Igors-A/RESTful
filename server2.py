# done by Igors Annastasjevs, fy18ia


import random
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import sqlite3, json, logging

logging.basicConfig(filename='log.txt', filemode='a', level=logging.DEBUG, format='%(asctime)s %(message)s')
app = Flask(__name__)  # set ups Flask-based server
api = Api(app)
con = sqlite3.connect('sources/gamedatas.db', check_same_thread=False)  # connects to database
cur = con.cursor()
cur.execute("SELECT * FROM games LIMIT 1")
top = cur.fetchall()[0]  # get keys for json/dictionary in order to sort information about the game from steam1.db

# gamedatas.db was created from steam.csv, which can be openly received from https://www.kaggle.com/nikdavis/steam-store-games?select=steam.csv
# gamedatas.db was slightly modified adding with more recent than data version appr. 5 games

def fromtupletodicofdb(t):  # function which basically explaining creates dictionary from tuple
    thegame = {}
    for i in range(len(top) - 7):  # columms from 12 to 18 were excess
        thegame.update({top[i]: t[i]})
    logging.debug('Created dictionary for '+thegame['name'])
    return thegame


class Agame():  # a game class, its "legacy" class as it was repurposed from storing 1 game into storing 1 game and 3 recommendations
    def __init__(self, game):
        logging.debug('Received title: ' + game)
        if '\'' in game:
            game = game[:game.index('\'')] + '\'' + game[game.index('\''):]
        cur.execute("SELECT * FROM games WHERE column2=" + "\'" + game + "\'")  # searches a game
        out = cur.fetchall()
        thegame = fromtupletodicofdb(out[0])
        genres = thegame['genres'].split(';')  # for recommendation getting
        # commands' generation
        if 'Sexual Content' in genres:
            """this was added because one of the games had this tag. The game, which names I tested, had 1% of 'Sexual Content',
            but it was enough for sqlite to present a lot of possibly pornographic games"""
            genres.remove('Sexual Content')
        command1 = "SELECT * FROM games WHERE (column10 LIKE \'%" + genres[0] + "%\'"
        if (len(genres) > 1):
            for i in range(1, len(genres)):
                command1 += " OR \'%" + genres[i] + "%\'"
        command1 += ") AND ( NOT column2=" + "\'" + game + "\')"
        tags = thegame['steamspy_tags'].split(';')  # for recommendation getting
        if 'Sexual Content' in tags:
            tags.remove('Sexual Content')
        if 'Nudity' in tags:
            tags.remove('Nudity')
        command2 = "SELECT * FROM games WHERE (column11 LIKE \'%" + tags[0] + "%\'"
        if (len(tags) > 1):
            for i in range(1, len(tags)):
                command2 += " OR \'%" + tags[i] + "%\'"
        command2 += ") AND ( NOT column2=" + "\'" + game + "\')"
        # receiving datas
        cur.execute(command1)
        out = cur.fetchall()#samples from genres
        cur.execute(command2)
        out2 = cur.fetchall()#sample from steamspy_tags
        for el in out2:#joins samples; sqlite does not provide A U B operation as 3 join operations in dqlite were tested
            if not(el in out):
                out.append(el)
        arr = []
        # random recommentations from array
        for i in range(0, 5):
            j = random.randint(0, len(out) - 1)
            arr.append(fromtupletodicofdb(out[j]))
        getout = {
            "the game": thegame,  # the game receive from client
            "recomm": arr  # array of recommended games
        }
        self.jsn = getout  # sents 'json'


class Sender(Resource):
    def get(self, game):
        self.a = Agame(game)  # getting data
        return self.a.jsn  # sending data

api.add_resource(Sender, '/sent/<game>')

if __name__ == '__main__':
    app.run(debug=True, port=7575)
