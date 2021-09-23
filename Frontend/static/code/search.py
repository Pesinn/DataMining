import requests
import json

def get_news_data(req):
  return requests.request("GET", f'http://10.94.63.91:8080/api/v1/news_data?{req}').json()
  
def get_news_data_from_file():
  file = open('static/test_data/articles.json',)
  data = json.load(file)
  file.close()

  return data