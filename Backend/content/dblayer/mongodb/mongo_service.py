import pymongo
import config
import json
import copy

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
  filter = {
    'named_entities': True,
    'sentiment_analysis': True,
    'articles': {'range': {'from': 1, 'to': 10, 'default': 10},
    'orderby': 'date'}
  }

  return get_news_data(search, filter)

def get_news_data(search, filter):
  if(config.get_db_collection() == "None"):
    return [x for x in load_json() if x['language'] == 'French' or x['language'] == 'English']
  else:
    if(config.DB_METHOD == "TEXT_SEARCH"):
      return get_news_data_text_search(search, filter)
    elif(config.DB_METHOD == "REGULAR_SEARCH"):
      return get_news_data_regular_search(search, filter)

def get_news_data_regular_search(search, filter):
  db_filter = create_db_filter(filter)
  query = regular_search_query(search)
  return [x for x in _mydb[NEWS].find(query, db_filter)]

def get_news_data_text_search(search, filter):
  search_list = []
  for i in search["search"]:
    new_obj = copy.deepcopy(search)
    new_obj["search"] = i
    search_list.append(new_obj)
  db_filter = create_db_filter(filter)
  data = []

  for i in search_list:
    query = text_search_query(i)
    data.append([x for x in _mydb[NEWS].find(query, db_filter)])

  return common_elements(data)

def common_elements(data):
  common_list = []
  length = len(data)
  for i in range(0,length):
    if(i == 0):
      common_list = data[i]
    else:
      common_list = get_common_elements(common_list, data[i])
  return common_list

def get_common_elements(list1, list2):
  if(list1 == [] or list2 == []):
    return []
  return [i for i in list1 if i in list2]


# https://www.analyticsvidhya.com/blog/2020/08/query-a-mongodb-database-using-pymongo/

def text_search_query(search):
  dbreq = []
  for i in search:
    query_object = {}
    query_object = query_parameter_to_search(query_object, search, i)
    
    if(i == "search"):
      query_object["$text"] = { "$search" : search[i] }

    dbreq.append(query_object)
  return {"$and": dbreq}

def regular_search_query(search):
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
                    {'keywords': {"$regex": a}}
                  ]
                }
        dbreq.append(query)

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
  db_filter = {"_id": 1,
            "description.text": 1,
            "title.text": 1,
            "article_language": 1,
            "publish_date": 1,
            "source": 1}
  if(filter == ""):
    return db_filter
  if(filter["sentiment_analysis"] == True):
    db_filter["annotations.sentiment_analysis"] = 1
  if(filter["named_entities"] == True):
    db_filter["annotations.entities.named"] = 1

  return db_filter