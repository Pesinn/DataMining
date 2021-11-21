import requests

def get_articles(req):
  data = get_articles_service(req)
  return data

def get_articles_service(req):
  return requests.request("GET", f'http://192.168.8.105:8080/api/v2/articles?{req}').json()