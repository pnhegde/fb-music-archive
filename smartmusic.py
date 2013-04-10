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

class SmartMusic:
    def __init__(self):
        self.con = Connection()["music"]["comments"]  # Open a connection with mongoDB

    def getSongs(self, num):
        songs = list(con.find().sort("name"))
        s = ""
        for song in songs:
            s = s+"<strong>" + song['name'] + '</strong>'+ '&nbsp&nbsp&nbsp&nbsp: &nbsp&nbsp&nbsp&nbsp <a href="'+song['message']+'" >' + song['pageTitle'] + " </a></br>"
        return s

