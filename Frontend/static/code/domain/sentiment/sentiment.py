import requests
import static.code.domain.news_data.news_data as news_data

def get_sentiment_analysis(req):
  data = get_sentiment_analysis_service(req)
  return data

def get_sentiment_analysis_file():
  return news_data.get_news_data_file()  

def get_sentiment_analysis_service(req):
  return requests.request("GET", f'http://192.168.8.105:8080/api/v1/sentiment?{req}').json()