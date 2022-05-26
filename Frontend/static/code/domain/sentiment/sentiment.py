import requests
import static.code.domain.news_data.news_data as news_data
import static.code.domain.sentiment.sentiment_factory as sent_fact
import static.code.domain.articles.articles_factory as art_fact
import config

def get_sentiment_analysis(req):
  data = get_sentiment_analysis_service(req)
  data = sent_fact.normalize_sentiment_analysis_arr(data)
  data = convert_search_from_array_to_string(data)
  return data, art_fact.get_total_articles_count(data)

def convert_search_from_array_to_string(data):
  for i in data:
    str = ""
    for x in i["search"]:
      str += x + ', '

    # Cut two last letters from the string
    size = len(str)
    if size > 2:
      str = str[:size - 2]

    i["search"] = str

  return data

def get_sentiment_analysis_file():
  return news_data.get_news_data_file()  

def get_sentiment_analysis_service(req):
  return requests.request("GET", f'{config.BACKEND_URL}/api/v1/sentiment?{req}').json()