from flask import Flask
from flask import request, jsonify, abort
from content.dblayer.dbservice import *

import os
import content.factory.request as req
import content.domain.news_data.news_data as domain_news_data
import content.domain.raw_data.raw_data as domain_raw_data

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


###########################
# News Data endpoints
###########################

@app.route('/api/v1/news_data', methods=['GET'])
def news_data():
  filter = req.create_filter(True, True, request)
  return req.get_news_data(request, filter)


###########################
# Raw Data endpoints
###########################

@app.route('/api/v1/raw_data', methods=['GET'])
def raw_data():
  search_arr = req.conv_req_to_search_array(request)
  return jsonify(domain_raw_data.get_raw_data(search_arr))


###########################
# Articles endpoints
###########################

@app.route('/api/v1/articles', methods=['GET'])
def articles():
  filter = req.create_filter(False, False, request)
  return get_news_data(request, filter)


###########################
# Entities endpoints
###########################

@app.route('/api/v1/entities', methods=['GET'])
def entities():
  filter = req.create_filter(True, False, request)
  return get_news_data(request, filter)


###########################
# Sentiment endpoints
###########################

@app.route('/api/v1/sentiment', methods=['GET'])
def sentiment_analysis():
  filter = req.create_filter(False, True, request)
  return get_news_data(request, filter)


###########################
# Helper functions
###########################

def get_news_data(request, filter):
  search_arr = req.conv_req_to_search_array(request)
  return jsonify(domain_news_data.get_news_data(search_arr, filter))


###########################
# Error handling
###########################

@app.errorhandler(404)
def resource_not_found(e):
  return jsonify(error=str(e)), 404

@app.errorhandler(400)
def resource_not_found(e):
  return jsonify(error=str(e)), 400


port = int(os.environ.get('PORT', 8080))
app.run(host='0.0.0.0', port=port)
