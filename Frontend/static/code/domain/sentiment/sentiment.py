import requests
import json

def get_sentiment_analysis_from_file():
  file = open('static/test_data/sentiment.json',)
  data = json.load(file)
  file.close()

  return data
