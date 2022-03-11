import requests
import json
import config

def get_news_data(req):
  return get_news_data_service(req)

def get_news_data_file():
  file = open('static/test_data/news_data.json',)
  data = json.load(file)
  file.close()

  return data

def get_news_data_service(req):
  return requests.request("GET", f'{config.BACKEND_URL}/api/v1/news_data?{req}').json()