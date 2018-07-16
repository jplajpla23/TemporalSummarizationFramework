# -*- coding: UTF-8 -*-

'''
Created on Oct 13, 2012

@author: samir
'''
import codecs
import urllib.request, urllib.error, urllib.parse
import simplejson
from . import SentimentBubbles

def getTweetsForLucene():

    """
        Returns a list of messages retrieved from a webservice
        request: url of webservice

    """

    listOfMessages = None


    request = "http://pattie.fe.up.pt/solr/portuguese/select/?q=Merkel&wt=json&rows=100"

    print("Getting new comments..\n")
    print("Requesting: " + request)

    opener = urllib.request.build_opener()
    data = opener.open(request)

    #Read the JSON response
    jsonResponse = simplejson.loads(str(data.read().decode("utf-8")))

    listOfMessages = []
    i = 0

    f = codecs.open("../Results/lucene.txt","w","utf-8")

    for message in jsonResponse["response"]["docs"]:

        i+=1

        print(message)
        text = str(message["text"]).replace("\t"," ").replace("\n"," ")
        try:
            friendCount = str(message["friends_count"])
        except KeyError:
            friendCount = "0"

        try:
            statusCount = str(message["statuses_count"])
        except KeyError:
            statusCount = "0"

        f.write(statusCount+"\t"+friendCount+"\t"+text+"\n")

        #listOfMessages.append(unicode(message["text"]))
    f.close()
    #print len(listOfMessages), " messages (of "+ str(i) + ") loaded\n"

    #store messages in cache for debugging


#    return listOfMessages


def main():

    tweets = SentimentBubbles.getComments("http://pattie.fe.up.pt/solr/portuguese/select/?q=Merkel&wt=json&rows=100")



    #populateSentiLists(sentiTokens)
    
if __name__ == '__main__':
    getTweetsForLucene()
    
    