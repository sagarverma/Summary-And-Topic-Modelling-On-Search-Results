#http://flask-restful-cn.readthedocs.org/en/0.3.4/quickstart.html
"""
    This is server program
"""
from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_restful import Resource, Api
import json, urllib, urllib2, unirest, re
from urllib2 import URLError, HTTPError 
from google import search
from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_restful import Resource, Api
import operator
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import summarize

app = Flask(__name__)

stopwordslist = stopwords.words("english")
wordnet_lemmatizer = WordNetLemmatizer()
ss = summarize.SimpleSummarizer()

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub(' ', text)

def remove_unicode(data):
    try:
        return data.decode('unicode_escape').encode('ascii','replace')
    except UnicodeDecodeError:
        return "UnicodeDecodeError"

def clean_document(data):
    data = re.sub(" \d+", " ", data)
    data = re.sub('\W+', ' ', data)
    return re.sub('\s+', ' ', data).strip()

def to_lower(data):
    return data.lower()

def remove_stopwords(words):
    return [word for word in words if word not in stopwordslist]

def lemmatize(words):
    word_occured_map = {}
    word_ret = []

    for word in words:
        word = wordnet_lemmatizer.lemmatize(word)
        if word not in word_occured_map:
            word_occured_map[word] = 1
            word_ret.append(word)

    return  word_ret

def showsome(searchfor):
  out = []

  for url in search(searchfor, stop=5):
    out.append(url)

  return out

def terms(data):
  response = unirest.post("https://sentinelprojects-skyttle20.p.mashape.com/",
    headers={
      "X-Mashape-Key": "Your-Key",
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

  all_terms = response.body["docs"][0]["terms"]

  ret = []

  for term in all_terms:
    ret.append(term['term'])
  
  return ret

def dummyTerms(data):
    words = data.split()
    words = remove_stopwords(words)
    words = lemmatize(words)

    word_freq = {}
    for word in words:
        if word not in word_freq:
            word_freq[word] = 1
        else: 
            word_freq[word] += 1

    sorted_x = sorted(word_freq.items(), key=operator.itemgetter(1))

    sorted_x = sorted_x[::-1]

    result = []
    if len(sorted_x) >= 10:
        for i in range(10):
            result.append(sorted_x[i][0])
    else:
        result = ['Error']

    return result


def getResult(links):
    result = {}
    for link in links:
        try:
            html = urllib2.urlopen("http://boilerpipe-web.appspot.com/extract?url="+link+"&extractor=ArticleExtractor&output=text&extractImages=")
            data = html.read()
            data = remove_unicode(data)
            data = remove_tags(data)

            summary = ss.summarize(data, 3)

            data = clean_document(data)
            data = to_lower(data)

            all_terms = dummyTerms(data)
            #all_terms = terms(data[:100])

            result[link] = [summary] + all_terms
        
        except URLError:
            pass

    return result

@app.route('/search', methods=['POST'])
def my_search():
    query = request.form['query']

    links = showsome(query)

    result = getResult(links)
    
    return jsonify({'result':result})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080)
    app.run(debug=True)