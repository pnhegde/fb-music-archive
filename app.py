#!venv/bin/python

# Standard Python imports
import json
import datetime
import bson.json_util
import urllib2

# SmartNotes imports
from smartnotes import SmartNotes

# Flask imports
from flask import Flask
from flask import request
from flask import render_template

# Pymongo imports
from pymongo import Connection

# Application configurations
DB_NAME = "snotes"  # Defines the database name for the application


snotes = SmartNotes(DB_NAME)  # Creates a SmartNotes object
app = Flask(__name__)  # Creates a Flask application object

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


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
        note = urllib2.unquote(request.form['note'])  # Fetching the note from the user request
    else:
        # GET request
       note = urllib2.unquote(request.args.get('note', ''))

    return insertNote(note, ipAddr, tStamp)


@app.route("/deletenote/", methods=['GET', 'POST'])
def deleteNote():
    """
        Deletes the note from the database
    """
    if request.method == 'POST':
        # POST request
        id = urllib2.unquote(request.form['id'])  # Fetching the id of note to delete from the user request
    else:
        # GET request
       id = urllib2.unquote(request.args.get('id', ''))

    return snotes.deleteNote(id)



@app.route("/similar/", methods=['GET', 'POST'])
def getSimilarNotes():
    """
        Return a set of similar notes
        based on the input id and topN
    """
    if request.method == 'POST':
        # POST request
        id = urllib2.unquote(request.form['id'])  # Fetching the id of note to delete from the user request
        topN = urllib2.unquote(request.form["topn"])
    else:
        # GET request
       id = urllib2.unquote(request.args.get('id', ''))
       topN = urllib2.unquote(request.args.get('topn', ''))

    results = snotes.getSimilarItems(id, topN)

    response =  {}
    response["success"] = "true"
    response["num"] = len(results)
    response["notes"] = []
    for (resultId, sim) in results:
        note = snotes.getNote(resultId)
        temp = {}
        temp["id"] = resultId
        temp["similarity"] = sim
        temp["note"] = note
        response["notes"].append(temp)

    return json.dumps(response)

@app.route("/getnote/", methods=['GET', 'POST'])
def getNote():
    """
        Returns the specified number of notes.
        if less returns everything.
    """
    if request.method == 'POST':
        # POST request
        num = urllib2.unquote(request.form['num'])  # Fetching the num of notes to be fetched
    else:
        # GET request
       num = urllib2.unquote(request.args.get('num', ''))  # Fetching the num of notes to be fetched

    notes = snotes.getNotes(int(num))

    print "got notes"
    response = {}
    response["success"] = "true"

    # Bug in pymongo?? !mportant <-- check this ASAP
    # response["num"] = notes.count()  # As notes is a cursor object (generator)

    response["notes"] = []

    count = 0
    for note in notes:
        # note is a dictionary here
        temp = {}
        print "each note"
        temp["id"] = str(note["_id"])
        print "got id"
        temp["note"] = note["note"]
        print "got note"
        response["notes"].append(temp)
        count += 1

    response["num"] = count

    return json.dumps(response)

@app.route("/updatenote/", methods=['GET', 'POST'])
def updateNote():
    """
        Updates the note with the
        new content without changing the id
    """
    if request.method == 'POST':
        # POST request
        id = urllib2.unquote(request.form['id'])  # Fetching the id of notes to be updated
        note = urllib2.unquote(request.form["note"])

    else:
        # GET request
       id = urllib2.unquote(request.args.get('id', ''))  # Fetching the id of notes to be updated
       note = urllib2.unquote(request.args.get('note', ''))

    return snotes.updateNote(id, note, request.remote_addr)

    
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