import pymongo
import config
import json

ARTICLES = "articles"

# Connect to the DB
_myclient = pymongo.MongoClient('localhost', 27017)
_dbList = _myclient.list_database_names()

# Create collection and DB
_mydb = _myclient[config.get_db_collection()]

# Used instead of the database connection
def load_json():
  file = open('content/dblayer/mongodb/test_data/articles.json',)
  data = json.load(file)
  file.close()
  return data

def get_articles(search):  
  if(config.get_db_collection() == "None"):
    return [x for x in load_json() if x['language'] == 'French' or x['language'] == 'English']
  else:
    filter = {"_id": 0}
    return [x for x in _mydb[ARTICLES].find(convert_search_obj_to_dbreq(search), filter)]

# https://www.analyticsvidhya.com/blog/2020/08/query-a-mongodb-database-using-pymongo/
def convert_search_obj_to_dbreq(search):
  dbreq = {}

  for i in search:
    if(i == "languages"):
      dbreq["language"] = { "$in" : search[i] }
    if(i == "sources"):
      dbreq["source"] = { "$in" : search[i] }
    if(i == "date_from"):
      dbreq["publish_date"] = { "$gt": search[i] }
    if(i == "date_to"):
      dbreq["publish_date"] = { "$lt": search[i] }
  return {"$or": [dbreq]}