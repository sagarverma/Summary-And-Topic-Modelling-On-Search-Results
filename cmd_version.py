import json, urllib, urllib2, unirest, re
from google import search
from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_restful import Resource, Api

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub(' ', text)

def remove_unicode(data):
    return data.decode('unicode_escape').encode('ascii','replace')

def clean_document(data):
    data = re.sub(r'\W+', ' ', data)
    return re.sub( '\s+', ' ', data).strip()

def to_lower(data):
    return data.lower()

def showsome(searchfor):
  out = []

  for url in search(searchfor, stop=5):
    out.append(url)

  return out

def terms(data):
  response = unirest.post("https://sentinelprojects-skyttle20.p.mashape.com/",
    headers={
      "X-Mashape-Key": "oO1AR6Dcy5mshuLMx1kF9yKU1cKrp1nXsMSjsna62QpvuuJ34E",
      "Content-Type": "application/x-www-form-urlencoded",
     "Accept": "application/json"
    },
    params={
     "annotate": 1,
     "keywords": 1,
     "lang": "en",
      "sentiment": 1,
     "text": data
    }
  )

  return response.body["docs"][0]["terms"]

app = Flask(__name__)

links = showsome("Latent Dirchlit Allocation")

for link in links:
  html = urllib2.urlopen(link)
  data = html.read()
  data = remove_unicode(data)
  data = remove_tags(data)
  data = clean_document(data)
  data = to_lower(data)
  #print data

  print terms(data[:100])
  