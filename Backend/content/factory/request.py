from re import search
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
      search_obj["search"].append(i.lower())    
    search_arr.append(search_obj)
  return search_arr