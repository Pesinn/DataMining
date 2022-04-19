import pymongo
import config
import json
import pprint
import copy

NEWS = "news_data"
FILTERS = "news_data_filters"

CLEAR_CACHE = True

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

def get_filters(name):
  return [x for x in _mydb[FILTERS].distinct(name)]

def get_news_data(search, filter):
  if CLEAR_CACHE == True:
    _mydb.command({
      "planCacheClear": NEWS
    })
  
  if(config.get_db_collection() == "None"):
    return [x for x in load_json() if x['language'] == 'French' or x['language'] == 'English']
  else:
    if(config.DB_METHOD == "CONJUNCTION_TEXT_SEARCH"):
      return get_news_data_text_search(search, filter)
    elif(config.DB_METHOD == "AGGREGATION_TEXT_SEARCH"):
      return get_news_data_aggregation_search(search, filter)
    elif(config.DB_METHOD == "REGULAR_SEARCH"):
      return get_news_data_regular_search(search, filter)

def get_news_data_aggregation_search(search, filter):
  query = aggregation_search_query(search, filter)
  data = [x for x in _mydb[NEWS].aggregate(query)]
  score_threshold = generate_text_score_threshold(len(search["search"]))
  # Filter data above the score threshold
  return [x for x in data if x["score"] > score_threshold]

def get_news_data_regular_search(search, filter):
  db_filter = create_db_filter(filter)
  query = regular_search_query(search)
  data = [x for x in _mydb[NEWS].find(query, db_filter)]
  return sort(data)

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
  
  c = common_elements(data)
  return sort(c)

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

def beautify_print(t):
  json_str = pprint.pformat(t)
  print(json_str)

def aggregation_search_query(search, filter):
  dbObj = []
  search_str = ""
  search_arr = []
  for i in search["search"]:
    search_str += i + " "

  search_arr.append({ "$text": { "$search": search_str.strip() } })

  for i in search:
    query_object = {}
    query_object = query_parameter_to_search(query_object, search, i)
    if(query_object != {}):
      search_arr.append(query_object)

  dbObj.append({ "$match": { "$and": search_arr } })

  project = create_db_filter(filter)
  project["score"] = {"$meta": "textScore"}

  dbObj.append({"$project": project})
  dbObj.append({ "$sort": { "score": { "$meta": "textScore" }, "posts": 1 } })

  return dbObj

def text_search_query(search):
  dbreq = []
  for i in search:
    query_object = {}
    query_object = query_parameter_to_search(query_object, search, i)
    if(i == "search"):
      query_object["$text"] = { "$search" : search[i] }

    if(query_object != {}):
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
        dbreq.append({'keywords': {"$regex": a}})
  
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
  db_filter = {}

  if(filter == ""):
    return db_filter
  
  filtering(filter, "id", "_id", db_filter)
  filtering(filter, "link", "link", db_filter)
  filtering(filter, "description_text", "description.text", db_filter)
  filtering(filter, "title_text", "title.text", db_filter)
  filtering(filter, "article_language", "article_language", db_filter)
  filtering(filter, "publish_date", "publish_date", db_filter)
  filtering(filter, "source", "source", db_filter)
  filtering(filter, "keywords", "keywords", db_filter)
  filtering(filter, "sentiment_analysis", "annotations.sentiment_analysis", db_filter)
  filtering(filter, "named_entities", "annotations.entities.named", db_filter)
  return db_filter

def filtering(obj, name, db_name, db_filter):
  try:
    if(obj[name] == True):
      db_filter[db_name] = 1
  except Exception as error:
    return ""

def generate_text_score_threshold(search_topics_len):
  return search_topics_len * 0.5

def sort(data):
  return sorted(data, key=lambda x: x["publish_date"], reverse=True)