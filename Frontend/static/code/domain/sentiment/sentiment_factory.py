import numpy as nu

def normalize_sentiment_analysis_arr(data):
  for i in data:
    if i["articles_count"]["total"] > 0:
      i = normalize_sentiment_analysis_obj(i)
  return data

def normalize_sentiment_analysis_obj(data):
  total = float(data["sentiment_analysis"]["compound"]["all"]["freq"])
  for i in data["sentiment_analysis"]["compound"]:
    data["sentiment_analysis"]["compound"][i]["norm"] = nu.round((float(data["sentiment_analysis"]["compound"][i]["freq"]) / total) * 100)
  return data