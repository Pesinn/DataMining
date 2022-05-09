import requests
import static.code.domain.news_data.news_data as news_data
import static.code.domain.sentiment.sentiment_factory as sent_fact
import static.code.domain.articles.articles_factory as art_fact
import config

def get_sentiment_analysis(req):
  data = get_sentiment_analysis_service(req)
  data = sent_fact.normalize_sentiment_analysis_arr(data)
  return data, art_fact.get_total_articles_count(data)

def get_sentiment_analysis_file():
  return news_data.get_news_data_file()  

def get_sentiment_analysis_service(req):
  return requests.request("GET", f'{config.BACKEND_URL}/api/v1/sentiment?{req}').json()