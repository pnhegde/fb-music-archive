#!/usr/bin/env python

import facebook
import re
import pymongo
from pymongo import Connection
import os
import unicodedata
import urllib
import BeautifulSoup

token = "BAACEdEose0cBAFm4SfbZBlp9TTAYZBrFRIrQW7cmz3pVlDkYJR9uZCZB7bZA440sZBbL6Ho4GqivWUZC0RJwVNffnnwpShsGtDZBVMridYsLdvuuWibIZAdVS"

def extract(comments):
	con = pymongo.Connection(os.getenv('MONGOHQ_URL'))
	collection = con['music']['comments']
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
			logger["pageTitle"] = BeautifulSoup.BeautifulSoup(urllib.urlopen(logger["message"])).title.string
			collection.insert(logger, safe=True)
def fetch():
	graph = facebook.GraphAPI(token)
	comments = graph.get_object("397729806942347/comments", limit=1000)
	data = comments["data"]
	extract(data)

if __name__ == '__main__':
	fetch()

