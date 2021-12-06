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

  try:
    if(article_range is None):
      article_range = [1,10]
    else:
      article_range = article_range.split(",")
      article_range[0] = int(article_range[0])
      article_range[1] = int(article_range[1])
  except:
    abort(400, description="article_range should "+
          "contain two numbers with a comma between")

  return {
    "named_entities": ner,
    "sentiment_analysis": sentiment,
    "articles": {
      "range": {
        "from": article_range[0],
        "to": article_range[1]
      },
      "orderby": "date"
    }
  }
