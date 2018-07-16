# -*- coding: UTF-8 -*-

'''
Created on Apr 13, 2011

@author: samir
'''

import pickle
import re

def getFromCache(filename):
    
    obj = None
    
    try:
        f = open(filename, "r")
        obj = pickle.load(f)
    except IOError:
        obj = None
        
    return obj

def putInCache(obj, filename):
    
    f = open(filename, "w")
    
    try:
        pickle.dump(obj,f, pickle.HIGHEST_PROTOCOL)
    except IOError:
        print("ERROR: Couldn't save cache...")
    


def tokenizeIt(text):
    
    """
        Basic tokenizer, finds all the words... 
    """
    
    regex = r'\w+'
    tokens = re.findall(regex,text,re.U)
    
    return tokens
    

if __name__ == '__main__':
    print(tokenizeIt("text te! teas te_te"))
    print("go")