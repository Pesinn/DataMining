import requests
import json

def get_sentiment_analysis_from_file():
  file = open('static/test_data/sentiment.json',)
  data = json.load(file)
  file.close()

  return data

def get_sentiment_analysis(req):
  return requests.request("GET", f'http://192.168.8.105:8080/api/v1/sentiment?{req}').json()