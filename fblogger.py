#!/usr/bin/env python

import facebook
import re
import pymongo
from pymongo import Connection
import os
import unicodedata
import urllib
import lxml.html
from xml.dom import minidom

token = "BAACEdEose0cBAKoXqoxihT0kdIsN2uRgJELsbYRk9Ye77YwegnZCZBUSfQs4jigoZACfF3SgKFZBrd8SDvrQ7vK1YuKpJcfl1NNWZBx3qRsMFr9ZBZBSv4WX0GAbylOpZCAJqNgbTanGZBJzpL5qM8rP6Q36jfnHnIJZC6X2UngMt05EFSvah1Vf3ZAbglzmp2xBJP7SdgF9JGiVxHxlpqKRTmKUPS2O407ovSvtYZCroHYlrAZDZD"

def extract(comments):
    con = Connectio('mongodb://pnhegde:appyfizz@dharma.mongohq.com:10017/music')
    collection = con['music']['archive']

    for comment in comments:
        logger = {}
        if isinstance(comment["message"], unicode):
            comment["message"] = unicodedata.normalize('NFKD', comment["message"]).encode('ascii','ignore')

        if "http://" in comment["message"] or "https://" in comment["message"]:
            url =  re.search("(?P<url>https?://[^\s]+)", comment["message"]).group("url")
            logger["name"] = comment["from"]["name"]
            logger["url"] = url
            logger["urlID"] = comment["id"]

        if logger:
            try:
                cursor = collection.find({'urlID': str(comment["id"])})
                if cursor.count() != 0:
                    print "already exist"
                    continue
                if "youtu" in logger['url'] :
                        vid = re.search(r"(youtube|youtu)\.(com|be)/(.*v=([^&]*)|([^&]*))", logger['url'])
                        videoId = ""
                        if vid.group(1) == "youtube" :
                            videoId = vid.group(4)
                        else:
                            videoId = vid.group(5)
                            print videoId
                        if videoId:
                            xmldoc = minidom.parse(urllib.urlopen('http://gdata.youtube.com/feeds/api/videos/'+videoId+'?v=2'))
                            title = xmldoc.getElementsByTagName('media:title')
                            cat = xmldoc.getElementsByTagName('media:category')
                            des = xmldoc.getElementsByTagName('media:description')
                            thumbnail = xmldoc.getElementsByTagName('media:thumbnail')[0]
                        else:
                            print "Error finding video ID"
                            continue
                        if title:
                            try:
                                logger['title']  = title[0].firstChild.nodeValue
                            except Exception, e:
                                continue
                        if  cat:
                            logger['category'] = cat[0].getAttribute('label')
                        if des:
                            logger['description'] = des[0].firstChild.nodeValue
                        if thumbnail:
                            logger['thumbnail']  = str(thumbnail.getAttribute('url'))
                else:
                    logger["title"] = lxml.html.parse(logger['url']).find(".//title").text

                collection.insert(logger, safe=True)
            except Exception, e:
                continue


def fetch():
    graph = facebook.GraphAPI(token)
    comments = graph.get_object("397729806942347/comments", limit=25)
    data = comments["data"]
    extract(data)


if __name__ == '__main__':
    fetch()

