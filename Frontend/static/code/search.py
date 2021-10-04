import requests
import json

def get_articles(req):
  return requests.request("GET", f'http://192.168.8.105:8080/api/v1/articles?{req}').json()

def get_news_data(req):
  return requests.request("GET", f'http://192.168.8.105:8080/api/v1/news_data?{req}').json()

def get_news_data_from_file():
  file = open('static/test_data/articles.json',)
  data = json.load(file)
  file.close()

  return data