import requests
import static.code.domain.news_data.news_data as news_data
import config
import numpy as nu

def get_sentiment_analysis(req):
  data = get_sentiment_analysis_service(req)
  data = normalize_sentiment_analysis_arr(data)
  return data

def get_sentiment_analysis_file():
  return news_data.get_news_data_file()  

def get_sentiment_analysis_service(req):
  return requests.request("GET", f'{config.BACKEND_URL}/api/v1/sentiment?{req}').json()

def normalize_sentiment_analysis_arr(data):
  for i in data:
    i = normalize_sentiment_analysis_obj(i)
  return data

def normalize_sentiment_analysis_obj(data):
  total = float(data["sentiment_analysis"]["compound"]["all"]["freq"])
  for i in data["sentiment_analysis"]["compound"]:
    data["sentiment_analysis"]["compound"][i]["norm"] = nu.round((float(data["sentiment_analysis"]["compound"][i]["freq"]) / total) * 100)
  return data