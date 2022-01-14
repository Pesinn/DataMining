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

def get_raw_data(search):
    filter = {"_id": 0}
    return [x for x in _mydb[NEWS].find(convert_search_obj_to_dbreq(search), filter)]

def get_news_data(search, filter):
  if(config.get_db_collection() == "None"):
    return [x for x in load_json() if x['language'] == 'French' or x['language'] == 'English']
  else:
    db_filter = create_db_filter(filter)
    return [x for x in _mydb[NEWS].find(convert_search_obj_to_dbreq(search), db_filter)]

# https://www.analyticsvidhya.com/blog/2020/08/query-a-mongodb-database-using-pymongo/

def convert_search_obj_to_dbreq(search):
  if(config.DB_METHOD == "TEXT_SEARCH"):
    return text_search(search)
  elif(config.DB_METHOD == "REGULAR_SEARCH"):
    return regular_search(search)

def text_search(search):
  dbreq = []
  for i in search:
    query_object = {}
    query_object = query_parameter_to_search(query_object, search, i)

    if(i == "search"):
      search_string = " ".join(str(x) for x in search[i])      
      if(search_string != ""):
        query_object["$text"] = { "$search" : search_string }

    dbreq.append(query_object)
  return {"$and": dbreq}

def regular_search(search):
  dbreq = []
  for i in search:
    query_object = {}
    query_object = query_parameter_to_search(query_object, search, i)

    if(query_object != {}):
      dbreq.append(query_object)

    if(i == "search"):
      for a in search[i]:
        query = {"$or":
                  [
                    {'title.text': {"$regex": a, "$options": "i"}},
                    {'description.text': {"$regex": a, "$options": "i"}}
                  ]
                }
        dbreq.append(query)
    
  print({"$and": dbreq})
  return {"$and": dbreq}
  
def query_parameter_to_search(query_object, search, i):
  if(i == "languages"):
    query_object["article_language"] = { "$in" : search[i] }
  if(i == "sources"):
    query_object["source"] = { "$in" : search[i] }
  if(i == "date_from"):
    try:
      query_object["publish_date"]["$gt"] = search[i]
    except:
      query_object["publish_date"] = { "$gt" : search[i] }
  if(i == "date_to"):
    try:
      query_object["publish_date"]["$lt"] = search[i]
    except:
      query_object["publish_date"] = { "$lt" : search[i] }
  return query_object

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