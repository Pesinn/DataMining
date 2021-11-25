from flask import Flask
from flask import url_for
from flask import request, jsonify, abort
from content.dblayer.dbservice import *

import os
import pymongo
import config
import content.factory.request as req
import content.domain.articles.articles as domain_articles
import content.domain.news_data.news_data as domain_news_data
import content.domain.raw_data.raw_data as domain_raw_data
import content.domain.entities.entities as domain_entities
import content.domain.sentiment.sentiment_analysis as domain_sentiment

app = Flask(__name__)
app.config["DEBUG"] = True


###########################
# News data endpoints
###########################

"""
{
  "search": "Tesla Inc",
  "sentiment_analysis": {
    "all": {
      "freq": 2
    },
    "high": {
      "freq": 0
    },
    "highest": {
      "freq": 0
    },
    "low": {
      "freq": 0
    },
    "lowest": {
      "freq": 0
    },
    "middle": {
      "freq": 2
    }
  },
  "ner": {
    "named": {
      "EU": { 
        "freq: 2
      },
      "US": { 
        "freq: 2
      },
      "Russia": { 
        "freq: 2
      },
      "Brazil": { 
        "freq: 2
      },
      "European Union": { 
        "freq: 2
      }
    }
  }
  "articles": {
    [
      {
        "description": {
            "text": "European Union envoys are close to finalizing...."
        },
        "publish_date": "2021-09-06T13:00:04",
        "source": "BBC",
        "title": {
            "text": "EU nears deal on opening borders that is likely to exclude US, Russia, Brazil"
        }
      },
      {
        "description": {
            "text": "Lille's Osimhen collects top Ligue 1 African honour"
        },
        "publish_date": "2021-09-04T13:28:01",
        "source": "BBC",
        "title": {
            "text": "Lille's Osimhen collects top Ligue 1 African honour"
        }
      }
    ]
  }
}
"""

def create_filter(ner, sentiment, article_limit, order_by):
  return {
    "named_entities": ner,
    "sentiment_analysis": sentiment,
    "articles": {
      "limit": article_limit,
      "orderby": order_by
    }
  }


###########################
# News Data endpoints
###########################

@app.route('/api/v1/news_data', methods=['GET'])
def news_data():
  filter = create_filter(True, True, 10, "date")
  return get_news_data(request, filter)


###########################
# Raw Data endpoints
###########################

@app.route('/api/v1/raw_data', methods=['GET'])
def raw_data():
  search_obj = req.conv_req_to_search_obj(request)
  return jsonify(domain_raw_data.get_raw_data(search_obj))


###########################
# Articles endpoints
###########################

@app.route('/api/v1/articles', methods=['GET'])
def articles():
  filter = create_filter(False, False, 10, "date")
  return get_news_data(request, filter)


###########################
# Entities endpoints
###########################

@app.route('/api/v1/entities', methods=['GET'])
def entities():
  filter = create_filter(True, False, 10, "date")
  return get_news_data(request, filter)


###########################
# Sentiment endpoints
###########################

@app.route('/api/v1/sentiment', methods=['GET'])
def sentiment_analysis():
  filter = create_filter(True, False, 10, "date")
  return get_news_data(request, filter)


###########################
# Helper functions
###########################

def get_news_data(request, filter):
  search_arr = req.conv_req_to_search_array(request)
  return jsonify(domain_news_data.get_news_data(search_arr, filter))


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


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


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
