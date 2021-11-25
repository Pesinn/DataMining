import content.dblayer.mongodb.mongo_service as mongodb

def get_raw_data(search):
  return mongodb.get_raw_data(search)

def get_news_data(search, filter):
  return mongodb.get_news_data(search, filter)