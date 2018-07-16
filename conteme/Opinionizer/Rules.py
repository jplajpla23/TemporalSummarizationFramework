# -*- coding: UTF-8 -*-

'''
Created on Oct 13, 2012

@author: samir
'''
from . import Preprocessor
import re
from . import Utils
import pprint

class Rules:
    
    QUANT_LIST = ['muito','mto','muita','mta', 'mt', 'muitíssimo','muitíssima', 'pouco','pouca', 'pouquíssimo','pouquíssima',
                 'bastante','completamente', 'imensamente', 'estupidamente', 'demasiado', 
                 'profundamente', 'perfeitamente', 'relativamente', 'simplesmente', 
                 'verdadeiramente', 'inteiramente', 'realmente', 
                 'sempre', 'smp', 'sp', 'mais', 'bem', 'altamente', 'extremamente', 'mesmo','mm','msm', 
                 'particularmente', 'igualmente', 'especialmente', 'quase', 'tão',
                 'absolutamente', 'potencialmente', 'aparentemente', 'exactamente', 'nada','nd',
                 ]
    
    VCOP_LIST = ['é', 'foi', 'era', 'será',
            'está', 'esteve', 'estava', 'estará',
            'continua', 'continuou', 'continuava', 'continuará',
            'permanece', 'permaneceu', 'permanecia', 'permanecerá',
            'fica', 'ficou', 'ficava', 'ficará',
            'anda', 'andou', 'andava', 'andará',
            'encontra-se', 'encontrou-se', 'encontrava-se', 'encontrar-se-á',
            'sente-se', 'sentiu-se', 'sentia-se', 'sentir-se-á',
            'mostra-se', 'mostrou-se', 'mostrava-se', 'mostrar-se-á',
            'revela-se', 'revelou-se','revelava-se', 'revelar-se-á',
            'torna-se', 'tornou-se', 'tornava-se', 'tornar-se-á',
            'vive', 'viveu', 'vivia', 'viverá'
           ]   
    
    NCLAS_LIST = ['pessoa',  'homem',  'rapaz',  'jovem',  'gajo',  'tipo',  'fulano',
             'jogador',  'atleta',  'futebolista', 'seleção',  'selecção',  'equipa',  
             'onze inicial',  'onze', 'treinador',  'mister',  'técnico',  'selecionador',  
             'seleccionador',  'capitão', 'árbitro',  'bandeirinha',  'fiscal de linha',  
             'juiz', 'ala',  'ala direito',  'ala esquerdo',  'médio',  'médio defensivo', 
             'médio ofensivo',  'atacante',  'avançado',  'avançado central', 
             'central',  'defesa',  'defesa direito',  'defesa esquerdo',
             'ponta de lança',  'guarda redes',  'guarda-redes',  'lateral', 
             'lateral direito',  'lateral esquerdo',  'extremo',  'médio',  'trinco',
             'político','politico' 
            ]
    
    VSUP_LIST = ['aparenta', 'aparentou', 'aparentava', 'aparentará',
            'apresenta','apresentou', 'apresentava', 'apresentará',
            'continua', 'continuou', 'continuava', 'continuará',
            'demonstra', 'demonstrou', 'demonstrava', 'demonstrará',
            'faz', 'fez', 'fazia', 'fará',
            'mostra', 'mostrou', 'mostrava', 'mostrará',
            'revela', 'revelou', 'revelava', 'revelará',
            'sente', 'sentiu', 'sentia', 'sentirá',
            'tem', 'teve', 'tinha', 'terá',
            'transparece', 'transpareceu', 'transparecia', 'transparecerá',
            'anda sob', 'andou sob', 'andava sob', 'andará sob', 
            'anda com', 'andou com', 'andava com', 'andará com'
            'entra em', 'entrou em', 'entrava em', 'entrará em',
            'está com', 'esteve com', 'estava com','estará com',
            'está em', 'uesteve em', 'estava em', 'estará em',
            'está sob', 'esteve sob', 'estava sob', 'estará sob'
            'fica com', 'ficou com', 'ficava com', 'ficará com'
            ]
    
    NEG_LIST = ['não','nao','ñ','n']
    UNS_LIST = ["um","uma","uns","umas"]
    
    LIST_CACHE = "cache/listCache.cache"
    SENTI_CACHE = "cache/sentiTokens.cache"
    
    #sentiList = {}
    def __init__(self,sentiTokens):
        
        self.OPTIONAL = '000000'
        self.sentiTokens = sentiTokens
        sentiList = self.populateSentiLists()
        self.rules = self._loadRules(sentiList)
        
    def populateSentiLists(self):
        
        """
            Create lists of words
            positive\negative adjectives
            positive\negative noun
            positive\negative idiomatic expressions
            positive\negative verbs
            
            returns: a dictionary in the format
            
            {
                "posAdjectives": Positive Adjectives,
                "neutAdjectives": Neutral Adjectives,
                "negAdjectives": Negative Adjectives, 
                "posNouns": Positive Nouns,
                "neutNouns": Neutral Nouns,
                "negNouns": Negative Nouns,
                "posVerbs": Positive Verbs,
                "neutVerbs": Neutral Verbs,
                "negVerbs": Negative Verbs,
                "posIdiom": Positive Idiomatic Expressions,
                "neutIdiom": Neutral Idiomatic Expressions,
                "negIdiom": Negative Idiomatic Expressions
            }
        """
        
        ADJECTIVE = "adj"
        NOUN = "n"
        IDIOMATIC_EXPR = "idiom"
        VERB = "v"    
        
        posAdjectives = []
        neutAdjectives = []
        negAdjectives = []
        
        posNouns = []
        neutNouns = []
        negNouns = []
        
        posVerbs = []
        neutVerbs = []
        negVerbs = []
        
        posIdiom = []
        neutIdiom = []
        negIdiom = []
        
        for sentiToken in self.sentiTokens:
            
            newTokens = list(sentiToken.tokens.keys())
            
            if sentiToken.polarity == str(1):
                
                if sentiToken.pos == ADJECTIVE:
                    #TODO: ensure that duplicate tokens are not inserted  
                    posAdjectives += newTokens 
                
                elif sentiToken.pos == NOUN:
                    posNouns += newTokens
                
                elif sentiToken.pos == IDIOMATIC_EXPR:
                    posIdiom += newTokens
                
                elif sentiToken.pos == VERB:
                    posVerbs += newTokens
                
            elif sentiToken.polarity == str(0):  
                              
                if sentiToken.pos == ADJECTIVE:
                    #TODO: ensure that duplicate tokens are not inserted  
                    neutAdjectives += newTokens
                
                elif sentiToken.pos == NOUN:
                    neutNouns += newTokens
                
                elif sentiToken.pos == IDIOMATIC_EXPR:
                    neutIdiom += newTokens
                
                elif sentiToken.pos == VERB:
                    neutVerbs += newTokens
                
            elif sentiToken.polarity == str(-1):                                  
                
                if sentiToken.pos == ADJECTIVE:
                    #TODO: ensure that duplicate tokens are not inserted  
                    negAdjectives += newTokens
                
                elif sentiToken.pos == NOUN:
                    negNouns += newTokens
                
                elif sentiToken.pos == IDIOMATIC_EXPR:
                    negIdiom += newTokens
                
                elif sentiToken.pos == VERB:
                    negVerbs += newTokens
        
        sentiLists = {}
        
        sentiLists["posAdjectives"] = posAdjectives
        sentiLists["neutAdjectives"] = neutAdjectives
        sentiLists["negAdjectives"] = negAdjectives 
        sentiLists["posNouns"] = posNouns
        sentiLists["neutNouns"] = neutNouns
        sentiLists["negNouns"] = negNouns
        sentiLists["posVerbs"] = posVerbs
        sentiLists["neutVerbs"] = neutVerbs
        sentiLists["negVerbs"] = negVerbs
        sentiLists["posIdiom"] = posIdiom
        sentiLists["neutIdiom"] = neutIdiom
        sentiLists["negIdiom"] = negIdiom
        
        #pprint.pprint(sentiLists)
        return sentiLists
    
    def isMatch(self,ruleElement,targetToken,ruleDebug=False):
        
        """
            Matches a rule step against a token
            If the rule step is a string make string comparison
            If the rule step is a list, see if the token belongs to the list
        """
        
        #TODO: throw an exception when the element is of another type
        if type(ruleElement) == str:
            
            if ruleDebug:
                print("comparing: ", targetToken , " and ", ruleElement)
            
            if ruleElement == targetToken:
                return True
            else:
                return False
            
        elif type(ruleElement) == list:
            
            if ruleDebug:
                
                if len(ruleElement) > 10:
                    rx = ruleElement[0:10]
                else:
                    rx = ruleElement
                
                print("comparing: ", targetToken , " and ", rx)
                
            if targetToken in ruleElement:
                return True
            else:
                return False
    
    def ignoreParticles(self,sentence):
        
        exclude = ['te','se','me']
        filtered = [ t for t in sentence if t not in exclude ]
        
        return filtered
    
    def applyRule(self,sentence,rule,ruleDebug=False):
        
        """
            Matches a sentence against a rule
            sentence: a sentence
            rule: a rule 
            ruleDebug: If true print some debug messages
            
            returns (True if match|False otherwise,list of matched tokens)
        """
        
        RULE_OFFSET = 2
        #TODO:ignorar os "te", "me" (mete-me, faz-te,...)
        #tokenz = tokenizeIt(Preprocessor.approximateAscii(sentence))
        tokenz = self.ignoreParticles(Utils.tokenizeIt(sentence))
        
        if ruleDebug:
            print("\n\ntokenz: ", tokenz)
            print("rule: ", rule[0])
            
            
        score = 0
        #rule starts at position 2 (0:info,1:polarity)
        currentStep = RULE_OFFSET
        currentTokenIndex = 0
        foundTokens = []
        
        while currentTokenIndex < len(tokenz):
            
            tok = str(tokenz[currentTokenIndex])
            
            if self.isMatch(rule[currentStep],tok,ruleDebug):
                
                score += 1
                currentStep +=1
                currentTokenIndex +=1
                foundTokens.append(tok)
                
                if ruleDebug:
                    print("it is good! step: ",currentStep - RULE_OFFSET, " score:", score)
            else:
                
                if self.OPTIONAL in rule[currentStep]:
                    currentStep +=1
                    score += 1
                else:
                    if ruleDebug:
                        print("fail")
                    
                    score = 0
                    currentStep = RULE_OFFSET
                    currentTokenIndex +=1
                    foundTokens = []
           
            if score == len(rule) - RULE_OFFSET:
                break
        
        if ruleDebug:     
            print("score: ",score)    
        
        isMatch = score == len(rule) - RULE_OFFSET 
        
        return (isMatch,foundTokens)
    
    def _loadRules(self,sentiList):
        
        """
            loads the lexic-syntactic rules
            sentiList: a dictionary in the format           
            
                {
                    "posAdjectives": Positive Adjectives,
                    "neutAdjectives": Neutral Adjectives,
                    "negAdjectives": Negative Adjectives, 
                    "posNouns": Positive Nouns,
                    "neutNouns": Neutral Nouns,
                    "negNouns": Negative Nouns,
                    "posVerbs": Positive Verbs,
                    "neutVerbs": Neutral Verbs,
                    "negVerbs": Negative Verbs,
                    "posIdiom": Positive Idiomatic Expressions,
                    "neutIdiom": Neutral Idiomatic Expressions,
                    "negIdiom": Negative Idiomatic Expressions
                }
            
            RULES:
            A rule is a list of values, that can be:
            a string
            a list of strings
            
            If a step is optional add the OPTIONAL constant to the list of strings 
            
            
            Note: The first two items are headers!
            first item: a description of the rule
            second item: the polarity of the rule 
        """
        
        #""" Ex: não é uma pessoa honesta """
        rule1 = ['Regra 1: [NEG] [VCOP] (um|uma) [NCLAS] [AJD+] -> Neg',
                 -1,
                 Rules.NEG_LIST,
                 Rules.VCOP_LIST,
                 Rules.UNS_LIST,
                 Rules.NCLAS_LIST,
                 sentiList["posAdjectives"]]
            
        #""" Ex: não é um tipo autoritário """
        rule2 = ['Regra 2: [NEG] [VCOP] um [NCLAS] [AJD-] -> Pos',
                 1,
                 Rules.NEG_LIST,
                 Rules.VCOP_LIST,
                 Rules.UNS_LIST,
                 Rules.NCLAS_LIST,
                 sentiList["negAdjectives"]]        
                
                
        #""" Ex: não é um bom político """        
        rule3 = ['Regra 3: [NEG] [VCOP] um [AJD+] [NCLAS] -> Neg',
                 -1,
                 Rules.NEG_LIST,
                 Rules.VCOP_LIST,
                 Rules.UNS_LIST,
                 sentiList["posAdjectives"],
                 Rules.NCLAS_LIST]
            
        #""" Ex: não é um mau político """ 
        rule4 = ['Regra 4: [NEG] [VCOP] um [AJD-] [NCLAS] -> Pos',
                 1,
                 Rules.NEG_LIST,
                 Rules.VCOP_LIST,
                 Rules.UNS_LIST,
                 sentiList["negAdjectives"],
                 Rules.NCLAS_LIST]
            
        #""" Ex: não é um idiota """    
        rule5 = ['Regra 5: [NEG] [VCOP] um [AJD-] -> Pos',
                 1,
                 Rules.NEG_LIST,
                 Rules.VCOP_LIST,
                 Rules.UNS_LIST,
                 sentiList["negAdjectives"]]
        
        #""" Ex: não é um embuste """        
        rule6 = ['Regra 6: [NEG] [VCOP] um [N-] -> Pos',
                 1,
                 Rules.NEG_LIST,
                 Rules.VCOP_LIST,
                 Rules.UNS_LIST,
                 sentiList["negNouns"]]
                
        #""" Ex: não foi nada sincero """
        rule7 = ['Regra 7: [NEG] [VCOP] [QUANT] [Adj+] -> Neg',
                 -1,
                 Rules.NEG_LIST,
                 Rules.VCOP_LIST,
                 Rules.QUANT_LIST,
                 sentiList["posAdjectives"]]
        
        #""" Ex: não é nada parvo """
        rule8 = ['Regra 8: [NEG] [VCOP] [QUANT] [Adj-] -> Pos',
                 1,
                 Rules.NEG_LIST,
                 Rules.VCOP_LIST,
                 Rules.QUANT_LIST,
                 sentiList["negAdjectives"]]
                
        #""" Ex: não foi coerente """
        rule9 = ['Regra 9: [NEG] [VCOP] [Adj+] -> Neg',
                 -1,
                 Rules.NEG_LIST,
                 Rules.VCOP_LIST,
                 sentiList["posAdjectives"]]
        
        #""" Ex: não é mentiroso """        
        rule10 = ['Regra 10: [NEG] (um|uma|0) [VCOP] [Adj-] -> Pos',
                  1,
                  Rules.NEG_LIST,
                  Rules.UNS_LIST + [self.OPTIONAL],
                  Rules.VCOP_LIST,
                  sentiList["negAdjectives"]]
                
        #""" Ex: não demonstrou um forte empenho """    
        rule11 = ['Regra 11: [NEG] [VSUP] (um|uma|0) [ADJ+|0] [N+] -> Neg',
                  -1,
                  Rules.NEG_LIST,
                  Rules.VSUP_LIST,
                  Rules.UNS_LIST + [self.OPTIONAL],
                  sentiList["posAdjectives"] + [self.OPTIONAL],
                  sentiList["posNouns"]]
                
        # """ Ex: não mostrou falta de coragem """    
        rule12 = ['Regra 12: [NEG] [VSUP] (falta|excesso) de [N+] -> Pos',
                  1,
                  Rules.NEG_LIST,
                  Rules.VSUP_LIST,
                  ["falta","excesso"],
                  "de",
                  sentiList["posNouns"]]
                       
        #""" Ex:  é um político desonesto """    
        rule13 = ['Regra 13: [VCOP] um [NCLAS] [AJD-] -> Neg',
                  -1,
                  Rules.VCOP_LIST,
                  Rules.UNS_LIST,
                  Rules.NCLAS_LIST,
                  sentiList["negAdjectives"]]
        
        #""" Ex:  é um tipo honesto """        
        rule14 = ['Regra 14: [VCOP] um [NCLAS] [AJD+] -> Pos',
                  1,
                  Rules.VCOP_LIST,
                  Rules.UNS_LIST,
                  Rules.NCLAS_LIST,
                  sentiList["posAdjectives"]]
                
        #""" Ex:  é um mau político """    
        rule15 = ['Regra 15: [VCOP] um [AJD-] [NCLAS] -> Neg',
                  -1,
                  Rules.VCOP_LIST,
                  Rules.UNS_LIST,
                  sentiList["negAdjectives"],
                  Rules.NCLAS_LIST]
        
        #""" Ex:  é um bom político """
        rule16 = ['Regra 16: [VCOP] um [AJD+] [NCLAS] ?Pos\-> ',
                  1,
                  Rules.VCOP_LIST,
                  Rules.UNS_LIST,
                  sentiList["posAdjectives"],
                  Rules.NCLAS_LIST]
                
        #""" Ex: é um perfeito idiota """    
        rule17 = ['Regra 17: [VCOP] um [AJD+|0] [AJD-] -> Neg',
                  -1,
                  Rules.VCOP_LIST,
                  Rules.UNS_LIST,
                  sentiList["posAdjectives"] + [self.OPTIONAL],
                  sentiList["negAdjectives"]]
        
        #""" Ex: é um verdadeiro desastre """
        rule18 = ['Regra 18: [VCOP] um [AJD+|0] [N-] -> Neg',
                  -1,
                  Rules.VCOP_LIST,
                  Rules.UNS_LIST,
                  sentiList["posAdjectives"] + [self.OPTIONAL],
                  sentiList["negNouns"]]
        
        #""" Ex: é um mau perdedor """        
        rule19 = ['Regra 19: [VCOP] um [AJD-] [AJD-] -> Neg',
                  -1,
                  Rules.VCOP_LIST,
                  Rules.UNS_LIST,
                  sentiList["negAdjectives"],
                  sentiList["negAdjectives"]]
                
        #""" Ex: é um idiota """    
        rule20 = ['Regra 20: [VCOP] um [AJD-] -> Neg',
                  -1,
                  Rules.VCOP_LIST,
                  Rules.UNS_LIST,
                  sentiList["negAdjectives"]]
                
        #""" Ex: é um embuste """    
        rule21 = ['Regra 21: [VCOP] um [N-] -> Neg',
                  -1,
                  Rules.VCOP_LIST,
                  Rules.UNS_LIST,
                  sentiList["negNouns"]]
                
        #""" Ex: é muito parvo """
        rule22 = ['Regra 22: [VCOP] [QUANT] [Adj-] -> Neg',
                  -1,
                  Rules.VCOP_LIST,
                  Rules.QUANT_LIST,
                  sentiList["negAdjectives"]]
                
        #""" Ex: foi extremamente sincero """    
        rule23 = ['Regra 23: [VCOP] [QUANT] [Adj+] -> Pos',
                  1,
                  Rules.VCOP_LIST,
                  Rules.QUANT_LIST,
                  sentiList["posAdjectives"]]
                
        #""" Ex: é mentiroso """        
        rule24 = [ 'Regra 24: [VCOP] [Adj-] -> Neg',
                  -1,
                  Rules.VCOP_LIST,
                  sentiList["negAdjectives"]]
                
        
        #""" Ex: foi coerente """   
        rule25 = ['Regra 25: [VCOP] [Adj+] -> Pos' ,
                  1,
                  Rules.VCOP_LIST,
                  sentiList["posAdjectives"]]
                        
        
        #""" Ex: o idiota do Sócrates """    
        #rule26 = [u'Regra: o [ADJ-] do TARGET -> Neg']
                
                  
        #""" Ex: demonstrou uma especial arrogância """ 
        rule29 = ['Regra 29: [VSUP] (um|uma|0) [ADJ+|0] [N-] -> Neg',
                  -1,
                  Rules.VSUP_LIST,
                  Rules.UNS_LIST + [self.OPTIONAL],
                  sentiList["posAdjectives"],
                  sentiList["negNouns"]]
                
        #""" Ex: demonstrou (uma|0) especial coragem """
        rule30 = ['Regra 30: [VSUP] (um|uma|0) [ADJ+|0] [N+] -> Pos',
                  1,
                  Rules.VSUP_LIST,
                  Rules.UNS_LIST + [self.OPTIONAL],
                  sentiList["posAdjectives"] + [self.OPTIONAL],
                  sentiList["posNouns"]]
                
        #""" Ex: não engana OU não agiu de má-fé """   
        rule31 = ['Regra 31: [NEG]|nunca [V-]|[IDIOM-] -> Pos',
                  1,
                  Rules.NEG_LIST +["nunca"],
                  sentiList["negAdjectives"]+sentiList["negIdiom"]]
                  
        #""" Ex: não está a mentir """        
        rule32 = ['Regra 32: [NEG]|nunca [VCOP] a [V-] -> Pos',
                  1,
                  Rules.NEG_LIST+["nunca"],
                  Rules.VCOP_LIST,
                  "a",
                  sentiList["negVerbs"]]
        
        #TODO: maybe colapse two rules (33 and 35) using the self.OPTIONAL for the "se" token
        #""" Ex: não brilhou OU não agiu da boa-fé """
        rule33 = ['Regra 33: [NEG]|nunca (se|0) [V+]|[IDIOM+] -> Neg',
                  -1,
                  Rules.NEG_LIST+["nunca"],
                  ["se",self.OPTIONAL],#TODO: maybe these tokens will be removed
                  sentiList["posVerbs"]+sentiList["posIdiom"]]
        
        #""" Ex: não se atrapalhou OU não se espetou ao comprido """
        rule34 = ['Regra 34: [NEG]|nunca se [V-]|[IDIOM-] -> Pos',
                  1,
                  Rules.NEG_LIST+["nunca"],
                  "se",#TODO: maybe these tokens will be removed
                  sentiList["negVerbs"]+sentiList["negIdiom"]]
        
        #""" Ex: não ter (muita|0) contestação """       
        rule37 = ['Regra 37: [NEG] [VSUP] [QUANT|0] [N-] -> Pos' ,
                  1,
                  Rules.NEG_LIST,
                  Rules.VSUP_LIST,
                  Rules.QUANT_LIST + [self.OPTIONAL],
                  sentiList["negNouns"]]                
           
        #""" Ex: não ter (muito|0) talento """
        rule38 = ['Regra 38: [NEG] [VSUP] [QUANT|0] [N+] -> Neg',
                  -1,
                  Rules.NEG_LIST,
                  Rules.VSUP_LIST,
                  Rules.QUANT_LIST + [self.OPTIONAL],
                  sentiList["posNouns"]]       
        
        #""" Ex: ter (muita|0) coragem"""
        rule39 = ['Regra 39: [VSUP] [QUANT|0] [N+] -> Pos',
                  1,
                  Rules.VSUP_LIST,
                  Rules.QUANT_LIST + [self.OPTIONAL],
                  sentiList["posNouns"]]        
                 
              
        #""" Ex: ter (muito|0) medo"""
        rule40 = ['Regra 40: [VSUP] [QUANT|0] [N-] -> Neg',
                  -1,
                  Rules.VSUP_LIST,
                  Rules.QUANT_LIST + [self.OPTIONAL],
                  sentiList["negNouns"]]            
        
        
        #""" Ex: excesso/falta de coragem"""
        rule41 = ['Regra 41: falta de [N+] -> Neg',
                  -1,
                  ["falta","excesso"],
                  "de",
                  sentiList["posNouns"]]    
        
        setOfRules = [
                      rule31,
                      rule33,
                      rule1,
                      rule14,
                      rule2,
                      rule13,
                      rule3,
                      rule16,
                      rule4,
                      rule15,
                      rule5,
                      rule20,
                      rule6,
                      rule21,
                      rule7,
                      rule23,
                      rule8,
                      rule22,
                      rule9,
                      rule25,
                      rule10,
                      rule24,
                      rule11,
                      rule30,
                      rule12,
                      rule41,
                      rule17,
                      rule18,
                      rule19,
                      rule29,
                      rule32,
                      rule34,
                      rule37,
                      rule40,                  
                      rule38,
                      rule39]
          
        return setOfRules
    
    def applyAllRules(self,sentence):
        
        """
            Apply rules sequentially until a match is found or
            after trying all rules
            
            sentence: a sentence
            returns: a tuple with the form (polarity,classification method,list of found sentiTokens) 
                    (None,'',[]) if no clue is matched
        """
        
        RULE_INFO = 0
        RULE_POLARITY = 1
        IS_MATCH = 0
        FOUND_TOKENS = 1
        
        for rule in self.rules:
            
            #print "trying to match rule: ", rule[RULE_INFO]
            
            matchResult = self.applyRule(sentence, rule,False)
            
            if matchResult[IS_MATCH]:
                
                foundTokens = matchResult[FOUND_TOKENS]
                ruleInfo = rule[RULE_INFO]
                polarity = rule[RULE_POLARITY]                
                
                return (polarity,ruleInfo,foundTokens)
        
        #It does not match any rule
        return (None,'',[])
            
