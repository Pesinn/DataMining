from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import request, jsonify
from flask import render_template

import multidict as multidict
from PIL import Image
import random
import numpy as np
from wordcloud import WordCloud

import os
import static.code.domain.articles.articles as domain_articles
import static.code.domain.sentiment.sentiment as domain_sentiment
import static.code.domain.entities.entities as domain_entities
import static.code.factory.request as req
import static.code.factory.pagination as page

generated_image_path = "static/generated_images/"

app = Flask(__name__)

sentiment_labels = [
    "Very negative, between -1 and -0.75",
    "Negative, between -0.75 and -0.25",
    "Neutral, between -0.25 and 0.25",
    "Positive, between 0.75 sand 1",
    "Very positive, between 0.25 and 0.75"
]

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

def random_string(random_chars=12, alphabet="0123456789abcdef"):
    r = random.SystemRandom()
    return ''.join([r.choice(alphabet) for i in range(random_chars)])

@app.route('/index',  methods=["GET"])
@app.route('/',  methods=["GET"])
def index():
  search_req = req.conv_req_to_query_string(request)
  f = get_filter()

  # If no search query has been entered
  if "[]" in search_req or not search_req:
    return render_template("default.html", filter = f)
  try:
    art = domain_articles.get_articles(search_req)    
    art[0]["article_pages"] = page.article_pagination(art[0], request)

    if "[]" in art:
      print("[]")
      return render_template("default.html", filter = f)
    return render_template("articles.html", filter = f, data = art[0])
  except Exception as error:
    print("Error", error)
    return render_template("default.html", filter = f)

@app.route('/entities', methods=["GET"])
def entities():
  search_req = req.conv_req_to_query_string(request)
  f = get_filter()
  
  # If no search query has been entered
  if "[]" in search_req or not search_req:
    return render_template("default.html", filter = f)
  ent = domain_entities.get_entities(search_req)

  id = 0
  for i in ent[0]["entities"]["named"]:
    i["id"] = f"entity_{id}"
    id = id + 1
 
  ent[0]["article_pages"] = page.article_pagination(ent[0], request)
  
  if "[]" in ent:
    return render_template("default.html", filter = f)
  return render_template("entities.html", filter = f, data = ent[0])

@app.route('/entities-cloud', methods=["GET"])
def entities_cloud():
  search_req = req.conv_req_to_query_string(request)
  f = get_filter()

  # If no search query has been entered
  if "[]" in search_req or not search_req:
    return render_template("default.html", filter = f)

  ent = domain_entities.get_entities(search_req)
  cloud_image_path = create_word_cloud(ent)
  return render_template("entities_cloud.html", filter = f, cloud_image = cloud_image_path)

@app.route('/sentiment', methods=["GET"])
def sentiment():
  bar_labels=sentiment_labels
  search_req = req.conv_req_to_query_string(request)
  f = get_filter()

  # If no search query has been entered
  if "[]" in search_req or not search_req:
    return render_template("default.html", filter = f)

  sentiment = domain_sentiment.get_sentiment_analysis(search_req)
  return render_template("sentiment.html", filter = f, labels=bar_labels, data=sentiment)

@app.route('/sentiment-stats', methods=["GET"])
def sentiment_stats():
  bar_labels=sentiment_labels
  search_req = req.conv_req_to_query_string(request)
  f = get_filter()
  
  # If no search query has been entered
  if "[]" in search_req or not search_req:
    return render_template("default.html", filter = f)

  sentiment = domain_sentiment.get_sentiment_analysis(search_req)
  return render_template("sentiment_stats.html", filter = f, labels=bar_labels, data=sentiment)

def get_filter():
  return {
    "languages":
    {
      "en": True,
      "fr": False,
      "es": False
    },
    "sources":
    {
      "9news.com.au": False,
      "france24.fr": False,
      "foxnews": False
    },
    "date_from": "2020-01-01",
    "date_to": "2020-01-01",
  }

def create_word_cloud(ent):
  x, y = np.ogrid[:300, :300]

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

port = int(os.environ.get('PORT', 5552))
app.run(host='0.0.0.0', port=port)
