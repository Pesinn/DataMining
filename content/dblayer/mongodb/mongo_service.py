import pymongo
import config
import json

ARTICLES = "articles"

# Connect to the DB
_myclient = pymongo.MongoClient('localhost', 27017)
_dbList = _myclient.list_database_names()

# Create collection and DB
_mydb = _myclient[config.get_db_collection()]

for i in _mydb.list_collection_names():
  print(i)


def connect():
  print("!!connect!!", config.ENV)

# Used instead of the database connection
def load_json():
  file = open('content/dblayer/mongodb/test_data/articles.json',)
  data = json.load(file)
  file.close()
  return data

def get_articles():
  # Get test data from file
  if(config.get_db_collection() == "None"):
    return load_json()
  else:
    return _mydb[ARTICLES].find()

for i in get_articles():
  print(i)