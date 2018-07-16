# -*- coding: UTF-8 -*-

'''
Created on Oct 14, 2012

@author: samir
'''

from . import Rules
from . import Utils
from . import SentiTokensHandler
from .Opinionizer import Opinionizer
import pprint

LIST_CACHE = "../cache/listCache.cache"
SENTI_CACHE = "../cache/sentiTokens.cache"

def testApplyAllRules():

    sentenceNoMatch = "O sócrates e passos coelho são bff"

    s1 = [[sentenceNoMatch,None],[" o sócrates não é uma pessoa honesta ",-1],
                                          ["o sócrates não é uma pessoa honesta",-1],
                                          ["o sócrates não é uma tipo honesto",-1]]

    s2 = [[sentenceNoMatch,None],[" o sócrates não é um tipo autoritário ",1],
                                          ["o sócrates não é uma tipo autoritário",1]]
    s3 = [[sentenceNoMatch,None],[" o sócrates não é um bom político ",-1],
                                          [" o sócrates ñ é um bom político ",-1]]

    s4 = [[sentenceNoMatch,None],[" o sócrates não é um mau político ",1]]
    s5 = [[sentenceNoMatch,None],[" o sócrates não é um idiota ",1],
                                          [" o sócrates n é um idiota ",1]]

    s6 = [[sentenceNoMatch,None],[" o sócrates não é um embuste ",1]]
    s7 = [[sentenceNoMatch,None],[" o sócrates não foi nada sincero ",-1]]
    s8 = [[sentenceNoMatch,None],[" o sócrates não é nada parvo ",1]]
    s9 = [[sentenceNoMatch,None],[" o sócrates não foi coerente ",-1]]
    s10 = [[sentenceNoMatch,None],[" o sócrates não é mentiroso ",1]]
    s11 = [[sentenceNoMatch,None],[" o sócrates não demonstrou um forte empenho ",-1]]
    s12 = [[sentenceNoMatch,None],[" o sócrates não mostrou falta de coragem ",1]]
    s13 = [[sentenceNoMatch,None],[" o sócrates é um político desonesto ",-1]]
    s14 = [[sentenceNoMatch,None],[" o sócrates é um tipo honesto ",1]]
    s15 = [[sentenceNoMatch,None],[" o sócrates é um mau político ",-1]]
    s16 = [[sentenceNoMatch,None],[" o sócrates é um bom político ",1]]
    s17 = [[sentenceNoMatch,None],[" o sócrates é um perfeito idiota ",-1]]
    s18 = [[sentenceNoMatch,None],[" o sócrates é um verdadeiro desastre ",-1]]
    s19 = [[sentenceNoMatch,None],[" o sócrates é um mau perdedor ",-1]]
    s20 = [[sentenceNoMatch,None],[" o sócrates é um idiota ",-1]]
    s21 = [[sentenceNoMatch,None],[" o sócrates é um embuste ",-1]]
    s22 = [[sentenceNoMatch,None],[" o sócrates é muito parvo ",-1]]
    s23 = [[sentenceNoMatch,None],[" o sócrates foi extremamente sincero ",1]]
    s24 = [[sentenceNoMatch,None],[" o sócrates é mentiroso ",-1]]
    s25 = [[sentenceNoMatch,None],[" o sócrates foi coerente ",1]]
    #s26 = [ruler.rule26,[sentenceNoMatch,None],[u" o idiota do sócrates ",-1]]
    s29 = [[sentenceNoMatch,None],[" o sócrates demonstrou uma especial arrogância ",-1]]
    s30 = [[sentenceNoMatch,None],[" o sócrates demonstrou uma especial coragem ",1],
                                            [" o sócrates demonstrou especial coragem ",1],
                                            [" o sócrates demonstrou um especial empenho ",1]]

    s31 = [[sentenceNoMatch,None],[" o sócrates não engana ",1],
                                            [" o sócrates não agiu de má-fé ",1],
                                            [" o sócrates não marcou golo ",1],
                                            [" o sócrates não marcou um golo ",1],
                                            [" o sócrates não marcou um único golo ",1]]

    s32 = [[sentenceNoMatch,None],[" o sócrates não está a papaguear ",1]]

    s33 = [[sentenceNoMatch,None],[" o sócrates não brilhou ",-1],
                                            [" o sócrates não agiu de boa-fé ",-1]]

    s34 = [[sentenceNoMatch,None],[" o sócrates não se atrapalhou ",1],
                                            [" o sócrates não espetou-se ao comprido ",1]]

    s35 = [[sentenceNoMatch,None],[" o sócrates não se sacrificou ",-1],
                                            [" o sócrates não saiu-se bem ",-1]]

    s37 = [[sentenceNoMatch,None],[" o sócrates não tem muita susceptibilidade ",1],
                                            [" o sócrates não tem susceptibilidade ",1]]

    s38 = [[sentenceNoMatch,None],[" o sócrates não tem muito talento ",-1],
                                            [" o sócrates não tem talento ",-1]]

    s39 = [[sentenceNoMatch,None],[" o sócrates tem muita coragem ",1],
                                            [" o sócrates tem coragem ",1]]

    s40 = [[sentenceNoMatch,None],[" o sócrates tem muito medo ",-1],
                                            [" o sócrates tem medo ",-1]]

    s41 = [[sentenceNoMatch,None],[" o sócrates tem falta de coragem ",-1],
                                            [" o sócrates tem falta de alegria ",-1],
                                            [" o sócrates tem excesso de confiança ",-1]]

    #s42 = [ruler.rule42,[sentenceNoMatch,0],[u"a culpa foi do sócrates",-1],[u" o culpado é o sócrates",-1]]


    testCases = [s1,
             s2,
             s3,
             s4,
             s5,
             s6,
             s7,
             s8,
             s9,
             s10,
             s11,
             s12,
             s13,
             s14,
             s15,
             s16,
             s17,
             s18,
             s19,
             s20,
             s21,
             s22,
             s23,
             s24,
             s25,
             #s26,
             s29,
             s30,
             #s31,
             s32,
             #s33,
             #s34,
             #s35,
             s37,
             s38,
             s39,
             s40,
             s41
             ]
            #s42

    #testCases = [s38]#s10,s38,s39]
    #idiomatic expressions: s31,s33,s34,s35
    #TODO: idiomatic expressions need another approach

    failures = []
    sentiLex = "../Resources/SentiLex-flex-PT03.txt"
    sentiExcept = "../Resources/SentiLexAccentExcpt.txt"

    op = Opinionizer(sentiLex,sentiExcept)

    print("Got them rules man!")

    SENTENCE = 0
    EXPECTED = 1
    RES_POLARITY = 0
    RES_INFO = 1

    i=0

    for test in testCases:

        for t in test:

            res = op.classifyWithClues(t[SENTENCE])

            #print t[SENTENCE]
            #print res[RES_INFO]

            if res[RES_POLARITY] != t[EXPECTED]:

                failures.append( (i,t[SENTENCE],t[EXPECTED],res) )
        i+=1

    if len(failures) > 0:

        for failure in failures:
            print(str(failure[0]), ") ", failure[1])
            print("expected:", str(failure[2])," got:", str(failure[3][RES_POLARITY]))
            print("rule: ", str(failure[3][RES_INFO]))
            print("\n--------------------\n")

        print(str(len(failures))," errors\n")

    else:
        print("All ok!")

if __name__ == '__main__':
    print("go")
    testApplyAllRules()
