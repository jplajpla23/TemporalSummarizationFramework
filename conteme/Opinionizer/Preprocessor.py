# -*- coding: UTF-8 -*-

import re
import unicodedata

def approximateAscii(s):
    
    """ Replace unicode chars with their ascii approximation
        ex: ç -> c
            ã,á,â -> a
    """
    
    return (''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))).replace('-',' ')

def removeURLs(sentence):
    
    """
        Replaces urls with the tag <URL>
    """
    
    regex = "(.?http://.+?)( |$)|(.?www\..+?)( |$)"
    
    return re.sub(regex," <URL> ",sentence)


def removeUsernames(sentence):
    
    """
        Replaces user mentions with the tag <USER>
    """
    
    regex = ".?@.+?( |$)"
    return re.sub(regex," <USER> ", sentence)

def separateSpecialSymbols(sentence):
    
    symbols = [",","!",":",";",".","-","_","+","*","@","£","#","$","\"","%","&","(",")","/","<",">","[","]","^","{","}","|","'","~","?"]
    
    newSentence = sentence
    
    for s in symbols:
        newSentence = newSentence.replace(s," "+s+" ")
        
    return newSentence