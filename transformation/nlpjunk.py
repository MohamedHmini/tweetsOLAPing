import requests
import json

from google.cloud import language
from google.oauth2 import service_account
from google.cloud.language import enums
from google.cloud.language import types



def ispos(sc,mg):
    return sc * mg > 0

def isneg(sc,mg):
    return sc * mg < 0

def ismixed(sc,mg):
    return -0.3 <= sc <= 0.3

def isneutral(sc,mg):
    return mg <= 2

supported = ['ar', 'zh', 'zh-Hant', 'nl', 'en', 'fr', 'de', 'id', 'it', 'ja', 'ko', 'pl', 'pt', 'es', 'th', 'tr', 'vi']


# Build language API client (requires service account key)
client = language.LanguageServiceClient.from_service_account_json('projectkey.json')
document = types.Document(
        content="this is just a test, i'm trying to pass exactly 20 words sentence! to test if google cloud will process it for content classification. the world is full of haterd we are so doomed we can't even understand ourselves let alone to understand the wild hidden structural evidence of the world.",
        type=language.enums.Document.Type.PLAIN_TEXT
    )

features = {
    'extract_syntax': False,
    'extract_entities': False,
    'extract_document_sentiment': True, 
    'extract_entity_sentiment': False,
    'classify_text': True,
}

try:
    response = client.annotate_text(document=document, features=features)
    sentiment = response.document_sentiment
    response = client.classify_text(document)
    categories = response.categories

    snt =  [{ 'magnitude': sentiment.magnitude, 'score':sentiment.score }]
    cats = []

    for category in categories:
        cats.append({'name':category.name, 'confidence': category.confidence})
            
    print(snt)
    print(cats)
except Exception as e:
    print(e)
    pass         