import requests
import static.code.domain.news_data.news_data as news_data
import config

def get_articles(req):
  data = get_articles_service(req)
  return data

def get_articles_file():
  return news_data.get_news_data_file()

def get_articles_service(req):
  print(req)
  return requests.request("GET", f'{config.BACKEND_URL}/api/v1/articles?{req}').json()