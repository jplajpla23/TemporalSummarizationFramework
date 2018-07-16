# -*- coding: UTF-8 -*-
'''
Created on Sep 11, 2012

@author: samir
'''
from . import confs
from . import Utils
from . import Preprocessor
from . import SentiTokens

SENTI_CACHE = "../cache/sentiTokens.cache"
#MESSAGE_CACH = "/Users/samir/Documents/workspace/NewOpinionizer/cache/mess.cache"

debug = True

#tokens to avoid because they are very ambiguous!
#TODO: consider refactoring this...
exclude = ['sao','são','bom','bem','ganhar','seguro']

#Changed! Will ignore the idiomatic expressions
def buildSentiQuickRef(sentiTokens):
    
    """
        Build a dictionary of sentiTokens for quick search
        this way we can match flexions of a sentiToken
        e.g., "jogou,jogar,jogando" they are all flexions of the
        lemma "jogar"
        
        sentiTokens: a list of SentiTokens
        returns: a dictionary with the format {flexion:sentiToken}
    """
    
    quickRef = {}
    
    for sentiToken in sentiTokens:

        #ignore idiomatic expressions
        if sentiToken.pos != "idiom":
            for flex in sentiToken.flexions:
                quickRef[flex] = sentiToken

    return quickRef

def extractSentiTokens(bagOfTokens,quickRef):    
    
    """
        Finds the ocurrence of sentiTokens in a bag-of-tokens
        
        bagOfTokens: a list of tokens
        quickRef: dictionary of sentiTokens for quick matching
        
        returns: a list of tupples in the form (flexion, sentiToken object)
    """
    
    foundSentitokens = []
    
    for token in bagOfTokens:
        normToken = token.lower().strip()
        
        try:
            #sentiToken = quickRef[normToken][0]
            sentiToken = quickRef[normToken]
        except KeyError:
            #if the token is not a sentiToken continue
            continue                

        #ignore multi word expressions
        if len(sentiToken.lemma.strip(' ').split(' ')) == 1:
            if sentiToken.lemma not in confs.ignoreLemmas:
                foundSentitokens.append( (token,sentiToken ) )

    return foundSentitokens   

def loadSentiTokens(sentiTokensPath,accentExceptionsPath):    

    
    return  SentiTokens.loadSentiTokens(sentiTokensPath,accentExceptionsPath)

def classCount(sentence,quickRef):
    
    """
        Counts the number of positive, neutrals 
        and negative tokens in a sentence
        
        sentence: a sentence
        quickRef: dictionary of sentiTokens for quick matching

        returns: a dictionary in the form: 
        { 'negatives': [frequency of negatives, [foundTokens] ], 
          'neutrals': [frequency of neutrals, [foundTokens] ], 
          'positives': [frequency of positives, [foundTokens] ] }
    """
    
    FLEXION = 0
    SENTI_TOKEN = 1
    FREQUENCY = 0
    FLEXIONS = 1
    
    classification = {"positives":[0,[]],"neutrals":[0,[]],"negatives":[0,[]]}
    
    #approximateAscii eliminates accents
    #this is good for reducing variations on how a word is written. e.g. "zézé", can be written "zéze","zeze","zezé",...
    bagOfTokens = Utils.tokenizeIt(Preprocessor.approximateAscii(sentence))
    sentiTokens = extractSentiTokens(bagOfTokens,quickRef)

    currentClass = ''
    
    for sts in sentiTokens:        
        
        if int(sts[SENTI_TOKEN].polarity) == -1:
            currentClass = "negatives"
        elif int(sts[SENTI_TOKEN].polarity) == 0:
            currentClass = "neutrals"
        elif int(sts[SENTI_TOKEN].polarity) == 1:
            currentClass = "positives"
        
        classification[currentClass][FREQUENCY] +=1
        classification[currentClass][FLEXIONS].append(sts[FLEXION])
        
    return classification

def formatPositivesNegatives(someSentiTokens):
    
    """
        Takes a list of tupples in the form (flexion, sentiToken object)
        and formats as a dictionary in the form {"positives":[positive tokens],"negatives":[negative tokens] }
    """
    
    FLEXION = 0
    SENTI_TOKEN = 1
    SENTI_TOKEN_COUNTER = 0
    FOUND_FLEXIONS = 1
    
    output = {"negatives":{},"positives":{}}
    
    for stk in someSentiTokens:
        
        if stk[SENTI_TOKEN].polarity == "-1":
            polarity = "negatives"
        elif stk[SENTI_TOKEN].polarity == "1":
            polarity = "positives"
        else:
            continue
                
        if stk[SENTI_TOKEN].lemma not in output[polarity]:
        
            #[counterForTheSentiToken,flexions]
            output[polarity][stk[SENTI_TOKEN].lemma] = [0,[]]
        
        #increment the counter for this sentiToken
        output[polarity][stk[SENTI_TOKEN].lemma][SENTI_TOKEN_COUNTER] += 1
        
        #add this flexion to the list
        if stk[FLEXION] not in output[polarity][stk[SENTI_TOKEN].lemma][FOUND_FLEXIONS]: 
            output[polarity][stk[SENTI_TOKEN].lemma][FOUND_FLEXIONS].append(stk[FLEXION])
            
    return output 
    
           
def main():     
        
    None
if __name__ == '__main__':   
    
    main()
    
