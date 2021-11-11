from flask import Flask
from flask_restful import Resource, Api
#import requests
from google_images_search import GoogleImagesSearch
app = Flask(__name__)
api = Api(app)

#old key: AIzaSyDXQh87f9oCrYnzgwe4rOHAj7daN0z1Ef0
#new key: AIzaSyBqGRyWj03v13mprwwVCh_XIbKa_c7MOB4
#cx: 915e27a2c2a3f48ff
gis = GoogleImagesSearch('AIzaSyBqGRyWj03v13mprwwVCh_XIbKa_c7MOB4', '915e27a2c2a3f48ff')
sp={
    'q':'...'
}#search parameters
gis.search(sp)
if __name__ == '__main__':
    app.run(debug=True)