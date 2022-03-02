from re import search
from flask import abort
import content.utils.string as string_utils

def handle_query_parameters(req):
  search_obj = {}
  if 'languages' in req.args:
    search_obj["languages"] = string_utils.string_to_array(req.args.get("languages"), ",")
  if 'date_from' in req.args:
    search_obj["date_from"] = req.args.get("date_from")
  if 'date_to' in req.args:
    search_obj["date_to"] = req.args.get("date_to")
  if 'sources' in req.args:
    search_obj["sources"] = string_utils.string_to_array(req.args.get("sources"), ",")
  if 'named_entities' in req.args:
    search_obj["named_entities"] = int(req.args.get("named_entities"))
  else:
    search_obj["named_entities"] = 10
  return search_obj

def conv_req_to_search_array(req):
  search_arr = []
  for r in string_utils.string_objects_to_array(req.args.get("search")):
    search_obj = handle_query_parameters(req)
    search_obj["search"] = []
    for i in r:
      search_obj["search"].append(i.lower().strip())
    search_arr.append(search_obj)
  return search_arr

def create_filter(ner, sentiment, request):
  article_range = request.args.get("articles_range")
  if article_range:
    article_range = article_range.replace("{", "")
    article_range = article_range.replace("}", "")
  
  # Default article range is 10
  def_range = 10
  try:
    if(article_range is None):
      article_range = [1,def_range]
    elif(article_range == "first"):
      article_range = [1, def_range]
    elif(article_range == "last"):
      article_range = ["", "last"]
    else:
      article_range = article_range.split(",")
      article_range[0] = int(article_range[0])
      article_range[1] = int(article_range[1])

    if(article_range[0] > article_range[1]):
      temp = article_range[1]
      article_range[1] = article_range[0]
      article_range[0] = temp
  except:
    abort(400, description="article_range should "+
          "contain two numbers with a comma between")

  return {
    "named_entities": ner,
    "sentiment_analysis": sentiment,
    "_id": True,
    "description_text": True,
    "title_text": True,
    "article_language": True,
    "publish_date": True,
    "source": True,
    "articles": {
      "range": {
        "from": article_range[0],
        "to": article_range[1],
        "default": def_range
      },
      "orderby": "date"
    }
  }

def create_raw_filter():
  return {
    "named_entities": True,
    "sentiment_analysis": True,
    "keywords": True,
    "_id": True,
    "description_text": True,
    "title_text": True,
    "article_language": True,
    "publish_date": True,
    "source": True,
    "articles": {
      "range": {
        "from": 1,
        "to": 10,
        "default": 10
      },
      "orderby": "date"
    }
  }