# -*- coding: UTF-8 -*-

'''
Created on Oct 16, 2012

@author: samir
'''

import operator
import urllib.request, urllib.error, urllib.parse
import simplejson
import codecs
from . import Utils
from . import Preprocessor
from . import confs
from . import SentiTokensHandler
import os
import json

os.chdir("/Users/arian/Developer/workspace/koi/workspace/Opinionizer/NewOpinionizer")
SENTI_CACHE = "../cache/sentiTokens.cache"
MESSAGE_CACH = "../cache/mess.cache"

debug = False

def main():

    #comments = getComments("http://pattie.fe.up.pt/solr/facebook/select/?q=in_reply_to_object_id:420280914701671&wt=json&rows=1000000")
        
    comments = getComments("http://pattie.fe.up.pt/solr/portuguese/select/?q=Merkel%20AND%20created_at%3A[NOW-7DAY%20TO%20NOW]&wt=json&rows=50000")

    bubbles = newSentimentBubbles(comments)
    writeResults(bubbles,confs.positiveBubbles,confs.negativeBubbles)

def getComments(request):
    
    """
        Returns a list of messages retrieved from a webservice
        request: url of webservice
        
    """    
    
    listOfMessages = None
    
    #when developing it is faster to just store the messages in disk so that
    #I don't have to wait for the webservice all the time
    if debug:
        listOfMessages = Utils.getFromCache(MESSAGE_CACH)
    
    if listOfMessages is not None:
        print("messages found on cache!")
        return listOfMessages
    else:
    
        print("Getting new comments..\n")    
        print("Requesting: " + request)
       
	#request = urllib2.urlencode(request) 
        #print request
	opener = urllib.request.build_opener()
        data = opener.open(request)
            
        #Read the JSON response
        jsonResponse = simplejson.loads(str(data.read().decode("utf-8")))  
                                    
        listOfMessages = []
        i = 0
        
        for message in jsonResponse["response"]["docs"]:
            
            i+=1
            
            if debug:
                print(message)
                
            listOfMessages.append(str(message["text"]))
                        
        print(len(listOfMessages), " messages (of "+ str(i) + ") loaded\n") 
        
        #store messages in cache for debugging
        Utils.putInCache(listOfMessages,MESSAGE_CACH) 
       
        return listOfMessages

    
def newSentimentBubbles(messages):
    
    """
        1. Tokenize each message and create a bag-of-tokens
        2. Count the sentiTokens present in the bag-of-tokens
        3. Returns a dictionary in the form {"positives":[positive tokens],"negatives":[negative tokens] }
    """
    

    bagOfTokens = []

    for message in messages:
        #approximateAscii eliminates accents
        #this is good for reducing variations on how a word is written. e.g. "zézé", can be written "zéze","zeze","zezé",...
        preProcessed = Preprocessor.removeUsernames(message)
        preProcessed = Preprocessor.approximateAscii(preProcessed)
        bagOfTokens += Utils.tokenizeIt(preProcessed)
    
    print("compute sentiTokens")
    

    #Try to load sentiTokens from a cache (it takes some time to load the sentiTokens from the lexic)
    sentiTokens = Utils.getFromCache(SENTI_CACHE)
    
    if sentiTokens == None:
        sentiTokens = SentiTokensHandler.loadSentiTokens(confs.sentiPath,confs.accentExcepPath)
        
    quickRef = SentiTokensHandler.buildSentiQuickRef(sentiTokens) 

    foundSentiTokens = SentiTokensHandler.extractSentiTokens(bagOfTokens, quickRef)
    formatedSentiTokens = SentiTokensHandler.formatPositivesNegatives(foundSentiTokens)

    return formatedSentiTokens


def writeResults(formatedTokens,positivesFile,negativesFile):

    """
        write results in two files:
            positivesFile: path for the file to store the positive tokens
            negativesFile: path for the file to store the negative tokens
        each line will the format: lemma,freq,[flex1;...;flexN]
        e.g.: "certo,7,certissimo;certo;certos;certa;"
    """

    #Write negative tokens to file
    negativeTopics = []
    positiveTopics = []
    
    negatives = codecs.open(negativesFile,"w","utf-8")
    
    #sort by frequency of the lemma
    negativeTokens = sorted(iter(formatedTokens["negatives"].items()), key=operator.itemgetter(1),reverse=True)
    
    id_ = 0
    for token in negativeTokens:
        id_=id_ + 1
        line = str(token[0])+","+str(token[1][0])
        
        topic = {"id":str(id_),
                "name": token[0].encode("UTF-8"),
                "sentiment":"negative",
                "count":str(token[1][0]),
                "forms":line}
                
        negativeTopics.append(topic)
        
    negatives.close()

    #Write positive tokens to file
    positives = codecs.open(positivesFile,"w","utf-8")

    #sort by frequency of the lemma
    positiveTokens = sorted(iter(formatedTokens["positives"].items()), key=operator.itemgetter(1),reverse=True)

    for token in positiveTokens:
        line = str(token[0])+","+str(token[1][0])

        for flexion in token[1][1]:
            line+=","+str(flexion)

        topic = {"id":str(id_),
                "name": token[0].encode("UTF-8"),
                "sentiment":"positive",
                "count":str(token[1][0]),
                "forms":line}
                
        positiveTopics.append(topic)

    positives.close()
    
    all_topics = negativeTopics + positiveTopics;
    finalTopicsJson = json.dumps(all_topics)
    
    ftopics = open('../Results/topics.json', 'w')
    ftopics.write(finalTopicsJson)
    ftopics.close()
    

if __name__ == "__main__":

    print("Hello world!")
    main()
