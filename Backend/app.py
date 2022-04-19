from flask import Flask
from flask import request, jsonify, abort
from content.dblayer.dbservice import *

import os
import content.factory.request as req
import content.domain.news_data.news_data as domain_news_data
import content.domain.raw_data.raw_data as domain_raw_data
import content.domain.filters.filters as domain_filters
import content.misc.logging as log

app = Flask(__name__)
app.config["DEBUG"] = True


###########################
# News Data endpoints
###########################

@app.route('/api/v1/news_data', methods=['GET'])
def news_data():
  filter = req.create_filter(True, True, request)
  return get_news_data(request, filter)


###########################
# Raw Data endpoint
###########################

@app.route('/api/v1/raw_data', methods=['GET'])
def raw_data():
  search_arr = req.conv_req_to_search_array(request)
  filter = req.create_raw_filter()
  return jsonify(domain_raw_data.get_raw_data(search_arr, filter))


###########################
# Articles endpoint
###########################

@app.route('/api/v1/articles', methods=['GET'])
def articles():
  filter = req.create_filter(False, False, request)
  return get_news_data(request, filter)


###########################
# Entities endpoint
###########################

@app.route('/api/v1/entities', methods=['GET'])
def entities():
  filter = req.create_filter(True, False, request)
  return get_news_data(request, filter)


###########################
# Sentiment endpoint
###########################

@app.route('/api/v1/sentiment', methods=['GET'])
def sentiment_analysis():
  log.log(request, "INFO")
  filter = req.create_filter(False, True, request)
  return get_news_data(request, filter)


###########################
# Filter endpoint
###########################

@app.route('/api/v1/filters', methods=['GET'])
def filters():
  log.log("get filters", "INFO")
  return jsonify(domain_filters.get_filters())


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
