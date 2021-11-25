import pymongo
import config
import json

NEWS = "news_data"

# Connect to the DB
_myclient = pymongo.MongoClient('localhost', 27017)
_dbList = _myclient.list_database_names()

# Create collection and DB
_mydb = _myclient[config.get_db_collection()]

# Used instead of the database connection
def load_json():
  file = open('content/dblayer/mongodb/test_data/news_data.json',)
  data = json.load(file)
  file.close()
  return data

def get_articles(search):
  #db.articles.find({},{_id:0, "source": 1,"publish_date": 1, "title.text":1, "description.text":1})
  if(config.get_db_collection() == "None"):
    return [x for x in load_json() if x['language'] == 'French' or x['language'] == 'English']
  else:
    filter = {"_id": 0, "source": 1, "publish_date": 1, "title.text": 1, "description.text": 1}
    return [x for x in _mydb[NEWS].find(convert_search_obj_to_dbreq(search), filter)]

def get_raw_data(search):
    filter = {"_id": 0}
    return [x for x in _mydb[NEWS].find(convert_search_obj_to_dbreq(search), filter)]

def get_news_data(search, filter):
  if(config.get_db_collection() == "None"):
    return [x for x in load_json() if x['language'] == 'French' or x['language'] == 'English']
  else:
    db_filter = create_db_filter(filter)
    return [x for x in _mydb[NEWS].find(convert_search_obj_to_dbreq(search), db_filter)]

def get_sentiment_analysis(search):
  filter = {"_id": 0,
            "description.text": 1,
            "title.text": 1,
            "article_language": 1,
            "publish_date": 1,
            "source": 1,
            "annotations.sentiment_analysis": 1}
  return [x for x in _mydb[NEWS].find(convert_search_obj_to_dbreq(search), filter)]

def get_named_entities(search):
  filter = {"_id": 0,
            "description.text": 1,
            "title.text": 1,
            "article_language": 1,
            "publish_date": 1,
            "source": 1,
            "annotations.entities.named": 1}
  return [x for x in _mydb[NEWS].find(convert_search_obj_to_dbreq(search), filter)]

# https://www.analyticsvidhya.com/blog/2020/08/query-a-mongodb-database-using-pymongo/
def convert_search_obj_to_dbreq(search):
  dbreq = {}
  for i in search:
    if(i == "languages"):
      dbreq["language"] = { "$in" : search[i] }
    if(i == "sources"):
      dbreq["source"] = { "$in" : search[i] }
    if(i == "date_from"):
      try:
        dbreq["publish_date"]["$gt"] = search[i]
      except:
        dbreq["publish_date"] = { "$gt" : search[i] }
    if(i == "date_to"):
      try:
        dbreq["publish_date"]["$lt"] = search[i]
      except:
        dbreq["publish_date"] = { "$lt" : search[i] }

    if(i == "search"):
      search_string = " ".join(str(x) for x in search[i])
      if(search_string != ""):
        dbreq["$text"] = { "$search" : search_string }
  return {"$and": [dbreq]}

def create_db_filter(filter):
  db_filter = {"_id": 0,
            "description.text": 1,
            "title.text": 1,
            "article_language": 1,
            "publish_date": 1,
            "source": 1}

  if(filter["sentiment_analysis"] == True):
    db_filter["annotations.sentiment_analysis"] = 1
  if(filter["named_entities"] == True):
    db_filter["annotations.entities.named"] = 1
  return db_filter