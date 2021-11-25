import requests
import static.code.domain.news_data.news_data as news_data

def get_articles(req):
  data = get_articles_service(req)
  return data

def get_articles_file():
  return news_data.get_news_data_file()

def get_articles_service(req):
  return requests.request("GET", f'http://192.168.8.105:8080/api/v1/articles?{req}').json()