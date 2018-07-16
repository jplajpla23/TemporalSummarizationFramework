# -*- coding: UTF-8 -*-

'''
Created on Oct 13, 2012

@author: samir
'''
import re
import pprint



#Clues
#
#Note: The first two items are headers!
#first item: a description of the rule
#second item: the polarity of the rule
#third item: a regex that detects a clue

hasPosInterjection = ["Positive Interjection",
                      1,
                      r'(\W|^)(g+o+l+o+|f+o+r[cç]+a+|b+r+a+v+o+|b+o+a+|l+i+n+d+o+|f+i+x+e+|m(ui)?to+ b[eo]+m+|co+ra+ge+m|v+i+v+a+|v+a+i+|v+a+m+o+s+( l[aá]+)?|bo+ra+ l[aá]+|e+spe+t[aá]+cu+lo+|u+a+u+|y+e+s+|l+o+v+e+|l+i+k+e+|n+i+c+e+|g+o+a+l+|t+h+a+n+k+s+|o+b+r+i+g+a+d+o+|sco+re+d?)(\W|$)']         
                     

hasNegInterjection = ["Negative Interjection",
                      -1,
                      r'(\W|^)(j[aá]+ fo+mo+s|que+ ma+u+|fo+sga-se|j[áa]+ che+ga+|so+co+rro+|u+i+|a+i+|o+h+|i+rr+a+|a+pre+|ra+i+o+s|mandem-no embora|sa+i da+[íi]+|tirem-no da[ií]|da+ss+|fo+ra+|m+e+r+d+a+|f+o+d+a+-*s+e*|(es)?t[áa] fdd|que no+jo+|cre+do+|(oh)?meu deus|u+i+|li+vra+|va+i+ a+ba+i+xo+|fo+ra+|(pa+ra+ a )?ru+a+|sa+fa+|cru+ze+s|pa+sso+u+-se|ba+sta+|fo+go+|esta+mo+s fe+i+to+s|fdx|c.?r.?l.?h.?|w+t+f+|f+u+c+k+)(\W|$)']         
    

hasPosSmiley = ["Happy Smiley",
                1,
                r'(\W|^)([\=:x8]-?[\)d\]]+)|<3(\W|$)'] 
     

hasNegSmiley = ["Sad Smiley",
                -1,
                r'(\W|^)[\=:x8]-?[\[\(s]+(\W|$)'] 

       
hasHeavyPunctuation = ["Heavy Punctuation",-1,
                       r'(\W|^)(!+\?+)|(\?+!+)(\W|$)'] 
    
setOfClues = [hasNegSmiley,hasHeavyPunctuation,hasPosInterjection,
              hasNegInterjection,hasPosSmiley] 

def findClues(sentence): 
    
    """
        Apply clue detectors sequentially until a match is found or
        after trying all clues
            
        sentence: a sentence
        returns: a tuple with the form (polarity,
                                        name of the match method,
                                        list of matched clues in the form (clue description,matched tokens) ) 
                 (None,'',[]) if no clue is matched
    """
    
    POLARITY = 1
    INFO = 0
    REGEX = 2
    foundClues = []
    score = 0
    
    for clue in setOfClues:
        
        match = re.search(clue[REGEX],sentence.lower())
    
        if match != None:
            
            foundClues.append((clue[INFO], match.group()))
            score += clue[POLARITY]
    
    if len(foundClues) > 0:
            
        return (score,'Clues',foundClues)
    else:
        return (None,'',[])

if __name__ == '__main__':  

    print("Go!")
    #clues = getClues()
    sentence = " :D isso é fixe!!? mas é mau raios :(( :((( :("
    res = findClues(sentence)
    
    print(pprint.pprint(res))       
        