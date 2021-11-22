import requests
import static.code.domain.news_data.news_data as news_data

def get_entities(req):
  data = get_entities_service(req)
  return data

def get_entities_file():
  return news_data.get_news_data_file()

def get_entities_service(req):
  return requests.request("GET", f'http://192.168.8.105:8080/api/v2/entities?{req}').json()