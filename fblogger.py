#!/usr/bin/env python

import facebook
import re
import pymongo
from pymongo import Connection
import os
import unicodedata
import lxml.html

token = "BAACEdEose0cBAAZBbG5vcL0E4uwM4ZBeHFGHWg2EGW9Vek0ZB1dNUsO858DmpHF2xZALgqZB02e0vupTRanW3896pN7P1IHWCaIWjViRf3z7i3V5xNpA6"

def extract(comments):
	con = pymongo.Connection(os.getenv('MONGOHQ_URL'))
	collection = con['comments']
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

