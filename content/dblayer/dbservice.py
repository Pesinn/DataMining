import content.dblayer.mongodb.mongo_service as mongodb

def get_news_data(search):
  return mongodb.get_news_data(search)