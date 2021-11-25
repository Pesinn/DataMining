import content.dblayer.mongodb.mongo_service as mongodb

def get_articles(search):
  return mongodb.get_articles(search)

def get_raw_data(search):
  return mongodb.get_raw_data(search)

def get_news_data(search, filter):
  return mongodb.get_news_data(search, filter)

def get_entities(search):
  return mongodb.get_named_entities(search)

def get_sentiment_analysis(search):
  return mongodb.get_sentiment_analysis(search)