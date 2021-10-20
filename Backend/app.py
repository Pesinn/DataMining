from flask import Flask
from flask import url_for
from flask import request, jsonify
from content.dblayer.dbservice import *

import os
import pymongo
import config
import content.factory.request as req
import content.domain.articles.articles as domain_articles
import content.domain.news_data.news_data as domain_news_data
import content.domain.entities.entities as domain_entities
import content.domain.sentiment.sentiment_analysis as domain_sentiment


app = Flask(__name__)
app.config["DEBUG"] = True

###########################
# Articles endpoints
###########################

@app.route('/api/v1/articles', methods=['GET'])
def articles():
  search_obj = req.conv_req_to_search_obj(request)
  return jsonify(domain_articles.get_articles(search_obj))


###########################
# News data endpoints
###########################

@app.route('/api/v1/news_data', methods=['GET'])
def news_data():
  search_obj = req.conv_req_to_search_obj(request)
  return jsonify(domain_news_data.get_news_data(search_obj))

###########################
# Entities endpoints
###########################

@app.route('/api/v1/entities', methods=['GET'])
def entities():
  search_obj = req.conv_req_to_search_obj(request)
  return jsonify(domain_entities.get_entities(search_obj))


###########################
# Sentiment endpoints
###########################

@app.route('/api/v1/sentiment', methods=['GET'])
def sentiment_analysis():
  search_arr = req.conv_req_to_search_array(request)
  return jsonify(domain_sentiment.get_sentiment_analysis(search_arr))


###########################
# Books endpoints
###########################

# Example: api/v1/resources/books/all
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
  return jsonify(books)

# Example: api/v1/resources/books?id=1
@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
  # Check if an ID was provided as part of the URL.
  # If ID is provided, assign it to a variable.
  # If no ID is provided, display an error in the browser.
  if 'id' in request.args:
      id = int(request.args['id'])
  else:
      return "Error: No id field provided. Please specify an id."

  # Create an empty list for our results
  results = []

  # Loop through the data and match results that fit the requested ID.
  # IDs are unique, but other fields might return many results
  for book in books:
      if book['id'] == id:
          results.append(book)

  # Use the jsonify function from Flask to convert our list of
  # Python dictionaries to the JSON format.
  return jsonify(results)





# Create some test data for our catalog in the form of a list of dictionaries.
books = [
  {'id': 0,
    'title': 'A Fire Upon the Deep',
    'author': 'Vernor Vinge',
    'first_sentence': 'The coldsleep itself was dreamless.',
    'year_published': '1992'},
  {'id': 1,
    'title': 'The Ones Who Walk Away From Omelas',
    'author': 'Ursula K. Le Guin',
    'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
    'published': '1973'},
  {'id': 2,
    'title': 'Dhalgren',
    'author': 'Samuel R. Delany',
    'first_sentence': 'to wound the autumnal city.',
    'published': '1975'}
]





port = int(os.environ.get('PORT', 8080))
app.run(host='0.0.0.0', port=port)
