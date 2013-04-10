#!/usr/bin/env python

import facebook
import re
import pymongo
from pymongo import Connection
import unicodedata
import lxml.html

token = "BAACEdEose0cBAPJ59ytZAetZBNd4ZBJ8OlTB6iOXYQz9DsyPZCIjDYQwdzXr2VfbiVBsZAcGuZB0wijMlXjvC2tvnr8QZCx4oGfe8bVZA5um9528dSN8hPbZA"

def extract(comments):
	collection = Connection()['music']['comments']
	for comment in comments:
		logger = {}
		if isinstance(comment["message"], unicode):
			comment["message"] = unicodedata.normalize('NFKD', comment["message"]).encode('ascii','ignore')
		if "http://" in comment["message"] or "https://" in comment["message"]:
			url =  re.search("(?P<url>https?://[^\s]+)", comment["message"]).group("url")
			logger["name"] = comment["from"]["name"]
			logger["message"] = url
			logger["comId"] = comment["id"]
		if logger:
			cursor = collection.find({'comId': str(comment["id"])})
			if cursor.count() != 0:
				print "already exist"
				continue
			logger["pageTitle"] =lxml.html.parse(logger['message']).find(".//title").text
			collection.insert(logger, safe=True)
def fetch():
	graph = facebook.GraphAPI(token)
	comments = graph.get_object("397729806942347/comments", limit=1000)
	data = comments["data"]
	extract(data)

if __name__ == '__main__':
	fetch()

