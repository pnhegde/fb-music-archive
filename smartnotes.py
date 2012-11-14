#!venv/bin/python

# Standard Python imports
import re
import bson
import json
import operator
import datetime
import math
import time

# NLTK imports
from nltk import PorterStemmer

# Pymongo imports
from pymongo import Connection

# Fuzzywuzzy imports
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class SmartNotes:
    """
        SmartNotes class defines the
        access functions to the mongodb
        database.
    """
    def __init__(self, dbName):
        """
            Initializes the application
            by creating the required database
            and collections.
        """
        self.con = Connection()  # Open a connection with mongoDB
        self.db = self.con[dbName]  # Get the reference to the db
        self.colNotes = self.db["notes"]  # Get the reference to the notes collection
        self.colSim = self.db["sim"]  # Get the reference to the sim collection

        # self.resetApplication()  # For testing. Will remove this later
        # self.initializeApplication()  # Initializes by adding a doc in 'sim' collection

        

        # ****** SCHEMA OF THE COLLECTIONS ***********
        # notes
        #   {
        #     "_id" : ObjectId("..."),
        #     "note" : "some sample note here",
        #     "tlist" : "sample, note",
        #     "ipaddr" : "127.0.0.1",
        #     "tstamp" : "dd/mm/yyyy-hh:mm:ss"
        # }
        #
        #
        # sim - type 1
        #   {
        #     "_id" : ObjectId("..."),
        #     "type" : "noteList",
        #     "noteList" : ["objID1", "objID2", "objID3", .....]   
        # }
        #
        # sim - type 2
        #   {
        #     "_id" : ObjectId("..."),
        #     "type" : "note",
        #     "similarity" : [
        #           {"objID1" : 0.69},
        #           {"objID2" : 0.78},
        #           .....
        #     ]
        # }
        # *********************************************

    def initializeApplication(self):
        """
            Initializes the database
            at the start of the application
        """
        self.colSim.insert({"type" : "noteList", "noteList" : []})  # Initializing 'sim' collection

    def resetApplication(self):
        """
            Deletes the entire database
            and initializes thr application
        """
        self.colNotes.remove({})
        self.colSim.remove({})

    def addNote(self,note):
        """
            Saves a note document into 
            the 'notes' collection and
            calculate similarity with all
            other notes.
        """
        note["ts"] = int(time.mktime(time.gmtime()))
        id = self.colNotes.insert(note)  # Insert the note into the database

        self.generateSimilarityMertic(str(id))  # update the similarity metic collection 'sim'

        return id

    def deleteNote(self, id):
        """
            Deletes a note from the database
        """
        
        try:
            int(id, 16)  # Check if passed id is a hex value
        except Exception, e:
            print e
            return json.dumps({"success" : "false", "id" : id})

        id = bson.objectid.ObjectId(id)
        self.colNotes.remove({"_id" : id})  # Delete an object based on Object id

        #Also remove from 'sim' collection
        self.colSim.remove({"_id" : id})
        # Update sim noteList and all other objects about removal
        # http://stackoverflow.com/questions/1740023/mongodb-how-to-update-multiple-documents-with-a-single-command
        # http://www.ryannitz.org/tech-notes/2009/08/10/mongodb-wildcard-query/
        self.colSim.update({"type" : "note"}, {"$pull" : {"similarity" : {str(id) : re.compile(".*")}}}, multi=True)  # Multi update (4th param true)

        # Update the noteList
        self.colSim.update({"type" : "noteList"}, {"$pull" : {"noteList" : str(id)}})

        # Successfully deleted. returning a bson object
        return json.dumps({"success" : "true", "id" : str(id)})

    def generateTerms(self, note):
        """
            generate a list of important terms
            from the note
        """

        # Stop words from http://www.textfixer.com/resources/common-english-words.txt
        stopWords = "a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your"
        stopWords = stopWords.split(",")

        # Replace all special symbols with spaces in the note
        note = re.sub('[^a-zA-Z0-9\n\.]', ' ', note)

        noteWords = note.split()  # Splits based on multiple spaces and tab!

        termList = []

        # Add only relevant words into term list
        for word in noteWords:
            # For each word, if not in stop words append to list
            if word.strip().lower() not in stopWords:
                termList.append(word.strip().lower())

        stemmedTermList = []
        # Stem the term list
        for word in termList:
            # For each word, stem it and append to list
            stemmedTermList.append(PorterStemmer().stem_word(word))

        return stemmedTermList

    def generateSimilarityMertic(self, id):
        """
            Generates a similarity metric
            between a note and all other notes
        """
        # Insert the current note to the 'sim' collection
        self.colSim.insert({"_id" : bson.objectid.ObjectId(id), "type" : "note", "similarity" : []})

        # Query db to fetch noteList
        response = self.colSim.find({"type" : "noteList"})
        print response

        #As we surely know that this query returns max=min=1 result
        # we can check this by len(response)
        noteList = response.next()["noteList"]  # This will return a list of note ids
        print noteList

        # For each note in that list
        # fetch its note, find similarity
        # update the current note's sim dict
        # update the new note's sim dict
        for noteId in noteList:
            # find similarity between noteA and noteB
            similarityValue = self.jaccardSimilarity(id, noteId)  # Sending both A and  B's note IDs

            # Store the similarity value in both noteA's list and noteB's list
            # Updating noteA
            self.colSim.update({"_id" : bson.objectid.ObjectId(id)}, {"$push" : {"similarity" : {noteId : str(similarityValue)}}})
            # Updating noteB
            self.colSim.update({"_id" : bson.objectid.ObjectId(noteId)}, {"$push" : {"similarity" : {id : str(similarityValue)}}})


        # Lastly, add the newly added note's id to the noteList
        self.colSim.update({"type" : "noteList"} , {"$push" : {"noteList" : id}})


    def jaccardSimilarity(self, noteAId, noteBId):
        """
            Finds the jaccard similarity
            between two notes
        """
        # fetch noteA terms using noteAId
        tListA = self.colNotes.find({"_id" : bson.objectid.ObjectId(noteAId)}).next()["tlist"]
        print tListA
        # fetch noteB terms using noteBId
        tListB = self.colNotes.find({"_id" : bson.objectid.ObjectId(noteBId)}).next()["tlist"]
        print tListB

        # Calculating basic jaccard similarity
        # js = intersection(a,b) / union(a,b)
        print set(tListA).intersection(set(tListB))
        try:
            similarity =  float(len(set(tListA).intersection(set(tListB)))) / float(len(set(tListA).union(set(tListB))))
        except Exception, e:
            print e
            similarity = 0.000001  # Setting to a very low value. Is this right? think!

        print similarity
        return similarity

    def getSimilarItems(self, id, topN):
        """
            Returns a list of topN
            notes similar to the note
            of the passed id
        """
        result = self.colSim.find({"_id" : bson.objectid.ObjectId(id)}, {"similarity" : 1, "_id" : 0}).next()["similarity"]
        sortedResult = {}

        # print result

        for rdict in result:
            # Send only non zero similarities
            if math.ceil(float(rdict.values()[0])) > 0:
                # Converting list of dictionaries
                # to a single dictionary
                sortedResult[rdict.keys()[0]] = float(rdict.values()[0])

        # print sortedResult
        # print(len(sortedResult))
        # print "*"*10
        # Sorting the dictionary
        # http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value
        return sorted(sortedResult.iteritems(), key=operator.itemgetter(1), reverse=True)
        # return dict(sorted(sortedResult.iteritems(), key=operator.itemgetter(1)).reverse())


    def getNote(self, id):
        """
            Returns the note for
            the id passed
        """
        return self.colNotes.find({"_id" : bson.objectid.ObjectId(id)}, {"_id" : 0, "note" : 1}).next()["note"]

    def getNotes(self, num):
        """
            Returns 'num' number of
            notes from the database
        """
        # Actually should return based on timestamp.
        # But at the moment will return top 'num' results
        return self.colNotes.find({}, {"_id" : 1, "note" : 1}, limit=num, sort=[("ts", -1)]) #.sort({"$natural" : -1}) # .limit(num)

    def updateNote(self, id, note, ipaddr):
        """
            Updates the contents, tags, 
            timestamp, ipaddr for a given id
        """
        # Remove old data
        self.colNotes.update({"_id" : bson.objectid.ObjectId(id)}, {"$unset" : { "note" : 1}})
        self.colNotes.update({"_id" : bson.objectid.ObjectId(id)}, {"$unset" : { "tlist" : 1}})
        self.colNotes.update({"_id" : bson.objectid.ObjectId(id)}, {"$unset" : { "ipaddr" : 1}})
        self.colNotes.update({"_id" : bson.objectid.ObjectId(id)}, {"$unset" : { "tstamp" : 1}})
        self.colNotes.update({"_id" : bson.objectid.ObjectId(id)}, {"$unset" : { "ts" : 1}})

        # Generating timestamp
        timeNow =  datetime.datetime.now()
        tStamp = '%s/%s/%s-%s:%s:%s' % (timeNow.month, timeNow.day, timeNow.year, timeNow.hour, timeNow.minute, timeNow.second)

        # Generating tlist
        tList = self.generateTerms(note)

        # Update new data
        self.colNotes.update({"_id" : bson.objectid.ObjectId(id)}, {"$set" : { "note" : note}})
        self.colNotes.update({"_id" : bson.objectid.ObjectId(id)}, {"$set" : { "tlist" : tList}})
        self.colNotes.update({"_id" : bson.objectid.ObjectId(id)}, {"$set" : { "ipaddr" : ipaddr}})
        self.colNotes.update({"_id" : bson.objectid.ObjectId(id)}, {"$set" : { "tstamp" : tStamp}})
        self.colNotes.update({"_id" : bson.objectid.ObjectId(id)}, {"$set" : { "ts" : int(time.mktime(time.gmtime()))}})

        # Updating sim
        #Also remove from 'sim' collection
        self.colSim.remove({"_id" : id})
        # Update sim noteList and all other objects about removal
        # http://stackoverflow.com/questions/1740023/mongodb-how-to-update-multiple-documents-with-a-single-command
        self.colSim.update({"type" : "note"}, {"$pull" : {"similarity" : {str(id) : re.compile(".*")}}}, multi=True)  # Multi update (4th param true)

        # Update the noteList
        self.colSim.update({"type" : "noteList"}, {"$pull" : {"noteList" : str(id)}})


        self.generateSimilarityMertic(str(id))

        response = {}
        response["success"] = "true"
        response["id"] = str(id)
        return json.dumps(response)


    def search(self, userQuery):
        """
            Searches the database for the query.
            The process is as follows.
            for each word 'input' in the query,
            input -> tolower -> remove stop words -> stem -> Levenshtein -> dblookup
        """
        # Stop words from http://www.textfixer.com/resources/common-english-words.txt
        stopWords = "a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your"
        stopWords = stopWords.split(",")

        # Replace all special symbols with spaces in the note and converitng to lowercase
        userQuery = re.sub('[^a-zA-Z0-9\n\.]', ' ', userQuery.lower())

        userQueryList = userQuery.split()  # Splits based on multiple spaces and tab!

        queryList = []

        # Removing stop words and stemming at one shot!
        for queryWord in userQueryList:
            if queryWord.strip() not in stopWords:
                queryList.append(PorterStemmer().stem_word(queryWord.strip()))

        print queryList
        noOfUserQueryWords = len(queryList)

        resultCount = {}
        resultForSorting = {}

        for query in queryList:
            # Query the DB, if present, add its id to resultCount

            pass  # Add Levenshtein fuzzy comparision here! ************

            results = self.colNotes.find({"tlist" : query},{"_id" :1, "note" : 1}, sort=[("ts", -1)])  #.sort({"ts" : -1})
            for result in results:
                if resultCount.has_key(str(result["_id"])):
                    # Update the count
                    resultCount[str(result["_id"])][1] += 1
                    resultForSorting[str(result["_id"])] += 1
                else:
                    # Update note contents and count
                    resultCount[str(result["_id"])] = [result["note"], 1]
                    resultForSorting[str(result["_id"])] = 1

        # Sorted results on frequency of occurence!
        sortedResults = sorted(resultForSorting.iteritems(), key=operator.itemgetter(1), reverse=True)

        response = {}
        response["success"] = "true"
        response["num"] = len(sortedResults)
        response["notes"] = []

        # ****** SEARCH RELEVANCE SCORE ******
        # The search relevance score is
        # calculated as follows
        #
        # if N is the number of valid input query terms
        # after removing stop words and M is the
        # number of matches for a note.
        #
        # then, the relevance of a note is calculated as,
        #
        # relevance = M / N
        #
        # if all terms match, then relevance = 1
        # if no terms match, then relevance = 0

        for (id, count) in sortedResults:
            temp = {}
            temp["id"] = id
            temp["score"] = float(count) / noOfUserQueryWords
            temp["note"] = resultCount[id][0]
            response["notes"].append(temp)

        return json.dumps(response)












        

