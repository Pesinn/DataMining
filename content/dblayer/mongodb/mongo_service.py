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

def get_articles():
  if(config.get_db_collection() == "None"):
    return [x for x in load_json() if x['language'] == 'French' or x['language'] == 'English']
  else:
    filter = {"_id": 0}
    return [x for x in _mydb[ARTICLES].find({
    "$or" : 
    [
      {
        "language" : { "$eq" : "English"}
      },
      {
        "language" : { "$eq" : "Spanish"}
      }
    ]
    }, filter)]

def create_filter():
  x = {
    "language": ["English", "Spanish"],
    "dateFrom": "2020-01-01",
    "dateTo": "2020-02-02",
    "sources": ["BBC", "CNN"],
    "search": ["Covid-19", "Alibaba Inc."]
  }
  return x