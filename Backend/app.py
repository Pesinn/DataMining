from flask import Flask
from flask import request, jsonify, abort
from content.dblayer.dbservice import *

import os
import time
import config
import content.factory.request as req
import content.domain.news_data.news_data as domain_news_data
import content.domain.raw_data.raw_data as domain_raw_data
import content.domain.filters.filters as domain_filters

app = Flask(__name__)
app.config["DEBUG"] = True


###########################
# News Data endpoints
###########################

@app.route('/api/v1/news_data', methods=['GET'])
def news_data():
  if config.TIME_MEASUREMENT == True:
    start = time.time()

  filter = req.create_filter(True, True, True, request)
  data = get_news_data(request, filter)

  if config.TIME_MEASUREMENT == True:
    end = time.time()
    time_elapsed = end - start
    print("API response time: ", time_elapsed)

  return data


###########################
# Raw Data endpoint
###########################

@app.route('/api/v1/raw_data', methods=['GET'])
def raw_data():
  if config.TIME_MEASUREMENT == True:
    start = time.time()

  search_arr = req.conv_req_to_search_array(request)
  filter = req.create_raw_filter()
  filter = req.create_filter(True, True, True, request)
  data = domain_raw_data.get_raw_data(search_arr, filter)

  if config.TIME_MEASUREMENT == True:
    end = time.time()
    time_elapsed = end - start
    print("API response time: ", time_elapsed)

  return jsonify(data)

###########################
# Keywords endpoint
###########################

@app.route('/api/v1/keywords', methods=['GET'])
def keywords():
  if config.TIME_MEASUREMENT == True:
    start = time.time()

  filter = req.create_filter(False, False, True, request)
  data = get_news_data(request, filter)

  if config.TIME_MEASUREMENT == True:
    end = time.time()
    time_elapsed = end - start
    print("API response time: ", time_elapsed)

  return data

###########################
# Articles endpoint
###########################

@app.route('/api/v1/articles', methods=['GET'])
def articles():
  if config.TIME_MEASUREMENT == True:
    start = time.time()

  filter = req.create_filter(False, False, False, request)
  data = get_news_data(request, filter)

  if config.TIME_MEASUREMENT == True:
    end = time.time()
    time_elapsed = end - start
    print("API response time: ", time_elapsed)

  return data

###########################
# Entities endpoint
###########################

@app.route('/api/v1/entities', methods=['GET'])
def entities():
  if config.TIME_MEASUREMENT == True:
    start = time.time()

  filter = req.create_filter(True, False, False, request)
  data = get_news_data(request, filter)

  if config.TIME_MEASUREMENT == True:
    end = time.time()
    time_elapsed = end - start
    print("API response time: ", time_elapsed)

  return data

###########################
# Sentiment endpoint
###########################

@app.route('/api/v1/sentiment', methods=['GET'])
def sentiment_analysis():

  if config.TIME_MEASUREMENT == True:
    start = time.time()

  filter = req.create_filter(False, True, False, request)
  data = get_news_data(request, filter)

  if config.TIME_MEASUREMENT == True:
    end = time.time()
    time_elapsed = end - start
    print("API response time: ", time_elapsed)
  
  return data


###########################
# Filter endpoint
###########################

@app.route('/api/v1/filters', methods=['GET'])
def filters():
  if config.TIME_MEASUREMENT == True:
    start = time.time()

  data = domain_filters.get_filters()

  if config.TIME_MEASUREMENT == True:
    end = time.time()
    time_elapsed = end - start
    print("API response time: ", time_elapsed)

  return jsonify(data)


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
