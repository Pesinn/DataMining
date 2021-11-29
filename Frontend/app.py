from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import request, jsonify
from flask import render_template

import multidict as multidict
from PIL import Image
import timeit
import re
import random
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

import io
import base64
import os
import static.code.domain.articles.articles as domain_articles
import static.code.domain.sentiment.sentiment as domain_sentiment
import static.code.domain.news_data.news_data as domain_news_data
import static.code.domain.entities.entities as domain_entities
import static.code.factory.request as req

generated_image_path = "static/generated_images/"

app = Flask(__name__)

sentiment_labels = [
    "Very negative, between -1 and -0.75",
    "Negative, between -0.75 and -0.25",
    "Neutral, between -0.25 and 0.25",
    "Positive, between 0.75 sand 1",
    "Very positive, between 0.25 and 0.75"
]
#t1 = timeit.Timer("''.join(random.choice('0123456789abcdef') for n in xrange(30))", "import random")


"""
[
  {
      "count": 7,
      "entity": "Daily Star",
      "type": "WORK_OF_ART"
  },
  {
      "count": 3,
      "entity": "Elon Musk",
      "type": "PERSON"
  },
  {
      "count": 2,
      "entity": "TESLA",
      "type": "ORG"
  }
]
"""
def getFrequencyDictForText(sentence):
  fullTermsDict = multidict.MultiDict()
  tmpDict = {}

  # making dict for counting frequencies
  for s in sentence:
    val = tmpDict.get(s["entity"], s["count"])
    tmpDict[s["entity"].lower()] = val + 1
  for key in tmpDict:
    fullTermsDict.add(key, tmpDict[key])
  return fullTermsDict
  

listing = [
  {
    "count": 7,
    "entity": "Daily Star",
    "type": "WORK_OF_ART"
  },
  {
    "count": 3,
    "entity": "Elon Musk",
    "type": "PERSON"
  },
  {
    "count": 2,
    "entity": "TESLA",
    "type": "ORG"
  }
]

def random_string(random_chars=12, alphabet="0123456789abcdef"):
    r = random.SystemRandom()
    return ''.join([r.choice(alphabet) for i in range(random_chars)])

@app.route('/index',  methods=["GET"])
@app.route('/',  methods=["GET"])
def index():
  search_req = req.conv_req_to_query_string(request)

  # If no search query has been entered
  if "[]" in search_req or not search_req:
    return render_template("default.html")

  art = domain_articles.get_articles(search_req)

  return render_template("articles.html", data = art)

def create_word_cloud(ent):
  x, y = np.ogrid[:300, :300]

  #mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
  #mask = 255 * mask.astype(int)
  cloud_mask = np.array(Image.open("static/images/cloud3.png"))

  image_freq = getFrequencyDictForText(ent[0]["entities"]["named"])

  wc = WordCloud(
    background_color="white",
    mask=cloud_mask
  )

  wc.generate_from_frequencies(image_freq)
  
  random_str = random_string()
  wc.to_file(f"{generated_image_path}{random_str}.png")
  
  return f"{generated_image_path}{random_str}.png"


@app.route('/entities', methods=["GET"])
def entities():
  search_req = req.conv_req_to_query_string(request)

  # If no search query has been entered
  if "[]" in search_req or not search_req:
    return render_template("default.html")

  ent = domain_entities.get_entities(search_req)

  id = 0
  for i in ent[0]["entities"]["named"]:
    i["id"] = f"entity_{id}"
    id = id + 1
  
  if "[]" in ent:
    return render_template("default.html")

  return render_template("entities.html", data = ent[0])

@app.route('/entities-cloud', methods=["GET"])
def entities_cloud():
  search_req = req.conv_req_to_query_string(request)

  # If no search query has been entered
  if "[]" in search_req or not search_req:
    return render_template("default.html")

  ent = domain_entities.get_entities(search_req)
  cloud_image_path = create_word_cloud(ent)
  return render_template("entities_cloud.html", cloud_image = cloud_image_path)

@app.route('/sentiment', methods=["GET"])
def sentiment():
  bar_labels=sentiment_labels
  search_req = req.conv_req_to_query_string(request)
  # If no search query has been entered
  if "[]" in search_req or not search_req:
    return render_template("default.html")

  sentiment = domain_sentiment.get_sentiment_analysis(search_req)
  print("sentiment", sentiment) 
  return render_template("sentiment.html", labels=bar_labels, data=sentiment)

@app.route('/sentiment-stats', methods=["GET"])
def sentiment_stats():
  bar_labels=sentiment_labels
  search_req = req.conv_req_to_query_string(request)

  # If no search query has been entered
  if "[]" in search_req or not search_req:
    return render_template("default.html")

  sentiment = domain_sentiment.get_sentiment_analysis(search_req)
  return render_template("sentiment_stats.html", labels=bar_labels, data=sentiment)

#@app.route('/books/', methods=["POST", "GET"])
#@app.route('/books/<id>', methods=["POST", "GET"])
#def books(id=None):
#    if(id!=None):
#        return render_template("books.html", books=getBookById(id))
#    return render_template("books.html", books=getBooks())

#def getBookById(id):
#    print("id: ", id)
#    response = requests.request("GET", f'http://192.168.8.105:8080/api/v1/resources/books?id={id}')
#    return response.json()

#def getBooks():
#    response = requests.request("GET", 'http://192.168.8.105:8080/api/v1/resources/books/all')
#    json_obj = response.json()
#    return json_obj

port = int(os.environ.get('PORT', 5555))
app.run(host='0.0.0.0', port=port)
