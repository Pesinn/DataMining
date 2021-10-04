import content.dblayer.mongodb.mongo_service as mongodb

def get_articles(search):
  return mongodb.get_articles(search)

def get_news_data(search):
  return mongodb.get_news_data(search)