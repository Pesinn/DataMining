from flask import Flask
from flask import request
from flask import render_template

import os
import static.code.domain.articles.articles as domain_articles
import static.code.domain.sentiment.sentiment as domain_sentiment
import static.code.domain.entities.entities as domain_entities
import static.code.factory.word_cloud as word_cloud
import static.code.factory.request as req
import static.code.factory.pagination as page
import static.code.factory.sentiment_decoration as sent_d

app = Flask(__name__)

@app.route('/index',  methods=["GET"])
@app.route('/',  methods=["GET"])
def index():
  pre_filter = req.conv_req_to_pre_filter(request)
  search_req = req.conv_pre_filter_to_query_string(pre_filter)
  domain_filter = req.pre_filter_to_domain_filter(pre_filter)
  # If no search query has been entered
  if "[]" in search_req or not search_req:
    return render_default(domain_filter)
  try:
    art = domain_articles.get_articles(search_req)
    art[0]["article_pages"] = page.article_pagination(art[0], request)
    if "[]" in art:
      return render_default(domain_filter)
    return render_template("articles.html", filter=domain_filter, data=art[0])
  except Exception as error:
    print("Error in route /", error)
    return render_default(domain_filter)
  
@app.route('/entities', methods=["GET"])
def entities():
  pre_filter = req.conv_req_to_pre_filter(request)
  search_req = req.conv_pre_filter_to_query_string(pre_filter)
  domain_filter = req.pre_filter_to_domain_filter(pre_filter)
  
  # If no search query has been entered
  if "[]" in search_req or not search_req:
    return render_default(domain_filter)
  ent = domain_entities.get_entities(search_req)

  id = 0
  for i in ent[0]["entities"]["named"]:
    i["id"] = f"entity_{id}"
    id = id + 1
 
  ent[0]["article_pages"] = page.article_pagination(ent[0], request)
  
  if "[]" in ent:
    return render_default(domain_filter)
  return render_template("entities.html", filter=domain_filter, data=ent[0])

@app.route('/entities-cloud', methods=["GET"])
def entities_cloud():
  pre_filter = req.conv_req_to_pre_filter(request)
  search_req = req.conv_pre_filter_to_query_string(pre_filter)
  domain_filter = req.pre_filter_to_domain_filter(pre_filter)
  
  # If no search query has been entered
  if "[]" in search_req or not search_req:
    return render_default(domain_filter)

  ent = domain_entities.get_entities(search_req)
  cloud_image_path = word_cloud.create_word_clouds(ent)
  return render_template("entities_cloud.html", filter=domain_filter, cloud_image=cloud_image_path)

@app.route('/sentiment', methods=["GET"])
def sentiment():
  bar_labels = sent_d.get_compound_sentiment_labels()
  graph_colors = sent_d.get_graph_colors()
  pre_filter = req.conv_req_to_pre_filter(request)
  search_req = req.conv_pre_filter_to_query_string(pre_filter)
  domain_filter = req.pre_filter_to_domain_filter(pre_filter)

  # If no search query has been entered
  if "[]" in search_req or not search_req:
    return render_default(domain_filter)

  sentiment = domain_sentiment.get_sentiment_analysis(search_req)
  return render_template("sentiment.html", filter=domain_filter, labels=bar_labels, data=sentiment, colors=graph_colors)

@app.route('/sentiment-ratio', methods=["GET"])
def sentiment_ratio():
  bar_labels = sent_d.get_text_ratio_sentiment_labels()
  graph_colors = sent_d.get_graph_colors()
  pre_filter = req.conv_req_to_pre_filter(request)
  search_req = req.conv_pre_filter_to_query_string(pre_filter)
  domain_filter = req.pre_filter_to_domain_filter(pre_filter)
  
  # If no search query has been entered
  if "[]" in search_req or not search_req:
    return render_default(domain_filter)

  sentiment = domain_sentiment.get_sentiment_analysis(search_req)
  return render_template("sentiment_ratio.html", filter=domain_filter, labels=bar_labels, data=sentiment, colors=graph_colors)

@app.route('/about', methods=["GET"])
def about():
  pre_filter = req.conv_req_to_pre_filter(request)
  domain_filter = req.pre_filter_to_domain_filter(pre_filter)
  return render_template("about.html", filter = domain_filter)

def render_default(f):
  return render_template("default.html", filter = f)

port = int(os.environ.get('PORT', 5551))
app.run(host='0.0.0.0', port=port)
