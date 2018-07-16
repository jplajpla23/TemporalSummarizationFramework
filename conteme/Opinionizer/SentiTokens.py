# -*- coding: UTF-8 -*-
'''
Created on Apr 12, 2011

@author: samir
'''

import codecs
from . import Utils
import re
from . import Preprocessor

class SentiToken:

    def __init__(self,lemma,polarity,pos,flexions=None):

        self.lemma = lemma
        self.polarity = polarity
        self.pos = pos
        self.flexions = []
        self.tokens = {}

        token = lemma.strip(' ').rstrip(' ')

        self.tokens[token] = ''
        multiword = token.replace(" ","_")

        #if ' ' was replaced with '_' then it's a multiword
        #so we also add the "multiword version" (with underscores instead of spaces)
        if "_" in multiword:
            self.tokens[multiword] = ''

        #for words with "-" generate a version without the "-"
        #and a version "multiword friendly" (with "_" instead of " ")
        if "-" in token and token not in self.tokens:
            self.tokens[token.replace("-"," ")] = ''
            self.tokens[token.replace("-","_")] = ''
            self.flexions.append(token.replace("-"," "))
            self.flexions.append(token.replace("-","_"))


        if flexions != None:

            for flexion in flexions:

                token = flexion.strip(' ').rstrip(' ')
                self.flexions.append(token)
                self.tokens[token] = ''

                multiword = token.strip(' ').rstrip(' ').replace(" ","_")

                if "_" in multiword:
                    self.flexions.append(multiword)
                    self.tokens[multiword] = ''

                #for words with "-" generate a version without the "-"
                #and a version "multiword friendly" (with "_" instead of " ")
                if "-" in token and token not in self.tokens:
                    self.tokens[token.replace("-"," ")] = ''
                    self.flexions.append(token.replace("-"," "))
                    self.flexions.append(token.replace("-","_"))
                    self.tokens[token.replace("-","_")] = ''

    def tostring(self):

        adj = "lemma: " + self.lemma + "\npolarity: " + self.polarity + "\nPOS:" + self.pos + "\nflexions: {"

        for f in self.flexions:

            adj += f+","

        return adj.strip(",") + "}"

    def isMatch(self,token):

            #return adjective == self.lemma or adjective in self.flexions
            return token in self.tokens

    def getTokens(self):

        return list(self.tokens.keys())


def loadSentiTokens(path,pathExceptions):

    f = codecs.open(path,"r", "utf-8")
    adjectives = []
    firstLine = next(f)
    exceptions = str(loadExceptionTokens(pathExceptions))

    lemmaRegex = ",(.*?)\."
    flexRegex = "^(.*?),"
    polarityRegex = "POL:..=(-1|0|1)(?:;|$)"
    posRegex = "PoS=(.*?);"

    currentLemma = re.search(lemmaRegex,firstLine).group(1)

    pol = re.findall(polarityRegex,firstLine)
    pol1 = int(pol[0])

    try:
        pol2 = int(pol[1])

    except IndexError:
        pol2 = 0

    currentPolarity = str(pol1 + pol2)

    currentPos = re.search(posRegex,firstLine).group(1).lower()
    currentFlex = re.search(flexRegex,firstLine).group(1)
    currentFlexions = []
    currentFlexions.append(currentFlex)

    if currentFlex not in exceptions and currentFlex != Preprocessor.approximateAscii(currentFlex):

        currentFlexions.append(Preprocessor.approximateAscii(currentFlex))

    for line in f:

        try:
            #ignore words marked as ambiguous
            if "REV=Amb" not in line:

                lemma = re.search(lemmaRegex,line).group(1)

                if lemma != currentLemma:

                    if currentLemma not in exceptions and currentLemma != Preprocessor.approximateAscii(currentLemma):

                        currentFlexions.append(Preprocessor.approximateAscii(currentLemma))

                    adjectives.append(SentiToken(currentLemma,currentPolarity,currentPos,currentFlexions))

                    currentLemma = lemma

                    pol = re.findall(polarityRegex,line)

                    pol1 = int(pol[0])

                    try:
                        pol2 = int(pol[1])

                    except IndexError:
                        pol2 = 0

                    currentPolarity = str(pol1 + pol2)

                    currentPos = re.search(posRegex,line).group(1).lower()
                    currentFlexions = []
                    currentFlex = re.search(flexRegex,line).group(1)
                    currentFlexions.append(currentFlex)

                    #print "L:", currentLemma,"P:",currentPolarity,"POS:",currentPos,"F:",currentFlex

                    if currentFlex not in exceptions and currentFlex != Preprocessor.approximateAscii(currentFlex):

                        currentFlexions.append(Preprocessor.approximateAscii(currentFlex))

                else:
                    currentFlex = re.search(flexRegex,line).group(1)
                    currentFlexions.append(currentFlex)

                    #print "l:", lemma, "f:", currentFlex, "p:", currentPos
                    if currentFlex not in exceptions and currentFlex != Preprocessor.approximateAscii(currentFlex):

                        currentFlexions.append(Preprocessor.approximateAscii(currentFlex))

        except:
            None
    f.close()

    return adjectives

def getMultiWords(listOfSentiTokens):

    multiWords = []

    for sentiToken in listOfSentiTokens:

        tokens = sentiToken.getTokens()

        for token in tokens:

            if token.find(" ") > 0:

                multiWords.append(token)

    return multiWords

def testGetPolarity():

    line = "abusa,abusar.PoS=V;FLEX=P:2s|P:4s|P:3s|Y:2s;TG=HUM:N0:N1;POL:N0=-1;POL:N1=0;ANOT=MAN"
    polarityRegex = "POL:..=(-1|0|1)(?:;|$)"
    m = re.findall(polarityRegex,line)
    print(m[0])
    print(m[1])

    #pol2 = int()


def loadExceptionTokens(path):

    f = codecs.open(path,"r", "utf-8")

    excpt = str(f.read())

    return excpt

if __name__ == "__main__":

    print("Go")


    #loadExceptionTokens("../Resources/SentiLexAccentExcpt.txt")
    f = codecs.open("res.txt","w","utf-8")

    sentiTokens = loadSentiTokens("Resources/SentiLex-flex-PT03.txt","Resources/SentiLexAccentExcpt.txt")


    for a in sentiTokens:

        None
        print("-----------------------")
        print(a.tostring().encode("utf-8"))
        print(">>")
        print(a.getTokens())


    print(len(sentiTokens))
    f.close()


    print("Done")
