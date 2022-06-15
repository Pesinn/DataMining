def get_total_articles_count(data):
  total = 0
  v_neg = 0
  neg = 0
  neu = 0
  pos = 0
  v_pos = 0

  for i in data:
    v_neg += i["sentiment_analysis"]["compound"]["lowest"]["freq"]
    neg += i["sentiment_analysis"]["compound"]["low"]["freq"]
    neu += i["sentiment_analysis"]["compound"]["middle"]["freq"]
    pos += i["sentiment_analysis"]["compound"]["high"]["freq"]
    v_pos += i["sentiment_analysis"]["compound"]["highest"]["freq"]
    total += i["articles_count"]["total"]

  return {
    "total": total,
    "v_neg": v_neg,
    "neg": neg,
    "neu": neu,
    "pos": pos,
    "v_pos": v_pos
  }