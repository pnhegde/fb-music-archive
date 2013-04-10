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
def getSong():
    if request.method == 'POST':
        # POST request
        num = urllib2.unquote(request.form['num'])  # Fetching the num of songs to be fetched
    else:
        # GET request
        num = urllib2.unquote(request.args.get('num', ''))  # Fetching the num of songs to be fetched

    #coll = pymongo.Connection(os.getenv('MONGOHQ_URL'))	
    con = pymongo.Connection()['music']['comments']
    songs = list(con.find().sort("name"))
    response = {}
    response["success"] = "true"

    response["songs"] = []

    count = 0
    for song in songs:
        print song
        temp = {}
        temp["id"] = str(song["comId"])
        temp["title"] = song["pageTitle"]
        temp["url"] = song["message"]
        temp["name"] = song["name"]
        response["songs"].append(temp)
        count += 1

    response["num"] = count
    return json.dumps(response)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
