import sys
import os
import requests
import json
import time

from google.cloud import language
from google.oauth2 import service_account
from google.cloud.language import enums
from google.cloud.language import types




class googleNLP_API:
    supported = ['ar', 'zh', 'zh-Hant', 'nl', 'en', 'fr', 'de', 'id', 'it', 'ja', 'ko', 'pl', 'pt', 'es', 'th', 'tr', 'vi']
    ispos  = lambda self,sc,mg:  sc * mg > 0
    isneg  = lambda self,sc,mg:  sc * mg < 0
    ismixed = lambda self,sc,mg:  -0.3 <= sc <= 0.3 and mg > 2
    isneutral = lambda self,sc,mg: -0.3 <= sc <= 0.3 and mg <= 2
    client = None

    def __init__(self):
        client = language.LanguageServiceClient.from_service_account_json('projectkey.json')
        self.client = client
    
    def sentimentInterpretation(self, sc, mg):
        if self.ismixed(sc,mg): return 'mixed'
        if self.isneutral(sc,mg): return 'neutral'
        if self.ispos(sc,mg): return 'positive'
        else : return 'negative'


    def getTextAnnotation(self, tx, lang):
        document = types.Document(
            content=tx,
            type=language.enums.Document.Type.PLAIN_TEXT,
            language = lang)
        
        features = {
            'extract_syntax': False,
            'extract_entities': False,
            'extract_document_sentiment': True, 
            'extract_entity_sentiment': False,
            'classify_text': lang == 'en' and len(tx.split(' ')) >= 20,
        }
        
        response = self.client.annotate_text(document=document, features=features)
        snt = response.document_sentiment
        cats = []
        if lang == 'en' and len(tx.split(' ')) >= 20:
            response = self.client.classify_text(document)
            cats = response.categories
    
        return snt.score, snt.magnitude, cats[0].name if len(cats) > 0 else None
    
    def process(self, tw):
        r = [None,None,None,None,None,None]
        if not (tw['lang'] in self.supported):
            return r
        
        stuff = self.getTextAnnotation(tw['text'], tw['lang'])
        
        r =[*stuff, stuff[0], stuff[1], self.sentimentInterpretation(stuff[0], stuff[1]), stuff[2].split('/')[1]]
        return r
    

