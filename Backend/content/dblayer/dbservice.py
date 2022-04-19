import config
import time
import content.dblayer.mongodb.mongo_service as mongodb

def get_news_data(search, filter):
  if config.TIME_MEASUREMENT == True:
    start = time.time()

  data = mongodb.get_news_data(search, filter)
  
  if config.TIME_MEASUREMENT == True:
    end = time.time()
    time_elapsed = end - start
    print("Database service response time: ", time_elapsed)

  return data

def get_filters(name):
  return mongodb.get_filters(name)