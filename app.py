#!venv/bin/python

import json
import datetime
import bson.json_util
import urllib2
import os

from flask import Flask
from flask import request
from flask import render_template

from pymongo import Connection

app = Flask(__name__)  # Creates a Flask application object

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/about/", methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route("/geturl/", methods=['GET', 'POST'])
def getUrl():
    coll = Connection("mongodb://pnhegde:appyfizz@dharma.mongohq.com:10017/music")
    conn = coll['music']['archive']
    songs = list(conn.find().sort("name").limit(50))
    response = {}
    response["success"] = "true"
    print response
    response["songs"] = []

    count = 0
    for song in songs:
        temp = {}
        temp["id"] = str(song["urlID"])
        temp["title"] = song["title"]
        temp["url"] = song["url"]
        temp['category'] = song["category"]
        temp['thumbnail'] = song["thumbnail"]
        temp["name"] = song["name"]
        response["songs"].append(temp)
        count += 1

    response["num"] = count
    return json.dumps(response)


# @app.route("/getCategory/", methods=['GET', 'POST'])
# def getCategory():
#     coll = Connection("mongodb://pnhegde:appyfizz@dharma.mongohq.com:10017/music")
#     conn = coll['music']['archive']
#     categories = list(conn.distinct('category'))
#     response = {}
#     response["success"] = "true"
#     print response
#     response["categories"] = categories
#     return json.dumps(response)


@app.route("/getComingSoon/")
def getComingSoon():
    return render_template('comingSoon.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
