import content.dblayer.mongodb.mongo_service as mongodb

def get_news_data(search, filter):
  return mongodb.get_news_data(search, filter)

def get_filters(name):
  return mongodb.get_filters(name)