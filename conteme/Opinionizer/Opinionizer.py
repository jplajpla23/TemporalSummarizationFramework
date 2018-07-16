# -*- coding: UTF-8 -*-
'''
Created on Oct 15, 2012

@author: samir
'''
from . import Utils
from . import SentiTokensHandler
from . import Preprocessor
from os import path
from .Rules import Rules
from . import Clues
import pprint

class Opinionizer:
    
    def __init__(self,sentiTokensPath=path.join(path.dirname(path.realpath(__file__)), 'Resources', 'SentiLex-flex-PT03.txt'),accentExceptionsPath=path.join(path.dirname(path.realpath(__file__)), 'Resources', 'SentiLexAccentExcpt.txt')):
        
        self.sentiTokens = SentiTokensHandler.loadSentiTokens(sentiTokensPath,accentExceptionsPath) 
        self.quickRef = SentiTokensHandler.buildSentiQuickRef(self.sentiTokens)
        self.ruleSet = Rules(self.sentiTokens)
    
    def simpleClassification(self,sentence):
        
        """
            Classify a sentence in terms of sentiment expressed
            The process consists of counting the sentiment tokens found
            on the sentence
            
            sentence: a sentence    
            returns: a tuple with the form (polarity,classification method,list of found sentiTokens)
                    (None,'',[]) if there is no match
        """
        
        FLEXION = 0
        SENTI_TOKEN = 1
        
        #approximateAscii eliminates accents
        #this is good for reducing variations on how a word is written. e.g. "zézé", can be written "zéze","zeze","zezé",...
        #Preprocessor.approximateAscii()
        bagOfTokens = Utils.tokenizeIt(sentence)
        sentiTokens = SentiTokensHandler.extractSentiTokens(bagOfTokens,self.quickRef)
        ocurrences = []
        polaritySum = 0
        
        for sts in sentiTokens:
            #TODO:the polarity property should be int
            polaritySum += int(sts[SENTI_TOKEN].polarity)
            ocurrences.append(sts[FLEXION])
        
        if len(ocurrences) > 0:
            
            if polaritySum > 0:
                polarity = 1
            elif polaritySum < 0:
                polarity = -1
            else:
                polarity = 0
            
            return (polarity,"simple classification",ocurrences)
        else:
            return(None,'',[])
        
    
    def classify(self,sentence):
       
        """
             Classify a sentence in terms of sentiment expressed
             Classification is performed in 3 levels:
             1. Try to match a lexic-syntactic rule
             2. If there is no match try to find syntactic clues such as smileys and interjections
             3. If there is no match classify by counting sentiTokens  
             
             sentence: a sentence    
             returns: a tuple with the form (polarity,classification method,list of found sentiTokens)
                     (None,'',[]) if there is no match
        """
        
        POLARITY = 0
        
        res = self.ruleSet.applyAllRules(sentence)
        
        if res[POLARITY] == None:
            res = Clues.findClues(sentence)        
        
        if res[POLARITY] == None:
            res = self.simpleClassification(sentence)
        
        return res
    
    

            
        
    
    
    
    
    
