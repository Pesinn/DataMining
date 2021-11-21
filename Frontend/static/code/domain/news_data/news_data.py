import requests
import json

def get_news_data(req):
  return get_news_data_service(req)

def get_news_data_file():
  file = open('static/test_data/news_data.json',)
  data = json.load(file)
  file.close()

  return data
  
def get_news_data_service(req):
  return requests.request("GET", f'http://192.168.8.105:8080/api/v2/news_data?{req}').json()