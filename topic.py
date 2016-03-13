import unirest


document = "So you're probably wondering how using Unirest makes creating requests in Python easier, let's start with a working example:"
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
    "text": document
  }
)

#print type(response.code)
#print type(response.headers)
print response.body["docs"][0]["terms"]
#print type(response.raw_body)