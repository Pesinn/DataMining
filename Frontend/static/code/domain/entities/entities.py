import requests
import static.code.domain.news_data.news_data as news_data
import config

def get_entities(req):
  data = get_entities_service(req)
  return data

def get_entities_file():
  return news_data.get_news_data_file()

def get_entities_service(req):
  return requests.request("GET", f'{config.BACKEND_URL}/api/v1/entities?{req}').json()