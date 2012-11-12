#!venv/bin/python

# Standard Python imports
import json
import datetime
import bson.json_util

# SmartNotes imports
from smartnotes import SmartNotes

# Flask imports
from flask import Flask
from flask import request

# Pymongo imports
from pymongo import Connection

# Application configurations
DB_NAME = "snotes"  # Defines the database name for the application


snotes = SmartNotes(DB_NAME)  # Creates a SmartNotes object
app = Flask(__name__)  # Creates a Flask application object

@app.route("/", methods=['GET', 'POST'])
def index():
    return "smartnotes! -- write notes the smart way!"


@app.route("/addnote/", methods=['GET', 'POST'])
def addNote():
    """
        Adds note to the database
    """

    ipAddr = request.remote_addr  # Fetching the user ip address from the request headers
        
    # Generating timestamp
    time =  datetime.datetime.now()
    tStamp = '%s/%s/%s-%s:%s:%s' % (time.month, time.day, time.year, time.hour, time.minute, time.second)

    if request.method == 'POST':
        # POST request
        note = request.form['note']  # Fetching the note from the user request
    else:
        # GET request
       note = request.args.get('note', '')

    return insertNote(note, ipAddr, tStamp)


@app.route("/deletenote/", methods=['GET', 'POST'])
def deleteNote():
    """
        Deletes the note from the database
    """
    if request.method == 'POST':
        # POST request
        id = request.form['id']  # Fetching the id of note to delete from the user request
    else:
        # GET request
       id = request.args.get('id', '')

    return snotes.deleteNote(id)



@app.route("/similar/", methods=['GET', 'POST'])
    """
        Return a set of similar notes
        based on the input id and topN
    """
    if request.method == 'POST':
        # POST request
        id = request.form['id']  # Fetching the id of note to delete from the user request
        topN = request.form["topn"]
    else:
        # GET request
       id = request.args.get('id', '')
       topN = request.args.get('topn', '')

    results = snotes.getSimilarItems(id, topN)

    response =  []
    for result in results:
        note = snotes.getNote(result)

    


    return json.dumps(response)  

    
def insertNote(note, ipAddr, tStamp):
    """
       this function generates terms from note and
       adds the contents of the note added 
       by user to the database by creating 
       a JSON object and returns the 
       response of inserting.
    """

    termList = snotes.generateTerms(note)

    try:
        # return json.dumps({
        #         "note" : note,
        #         "tlist" : termList,
        #         "ipaddr" : ipAddr,
        #         "tstamp" : tStamp
        #     })
        # Form a JSON object and add the note
        id = snotes.addNote({
                "note" : note,
                "tlist" : termList,
                "ipaddr" : ipAddr,
                "tstamp" : tStamp
            })

        return json.dumps({"success" : "true", "id" : str(id)})  # Using bson specific dump to serialize object id

    except Exception, e:
        # Unable to add the note. Some error
        print e
        return json.dumps({"success" : "false"})

    


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)