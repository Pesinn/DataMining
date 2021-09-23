import content.utils.string as string_utils

def conv_req_to_search_obj(req):
  search_obj = {}
  if 'languages' in req.args:
    #search_obj["languages"] = req.args.getlist("languages")
    search_obj["languages"] = string_utils.string_to_array(req.args.get("languages"), ",")
  if 'date_from' in req.args:
    search_obj["date_from"] = req.args.get("date_from")
  if 'date_to' in req.args:
    search_obj["date_to"] = req.args.get("date_to")
  if 'sources' in req.args:
    #search_obj["sources"] = req.args.get("sources")
    search_obj["sources"] = string_utils.string_to_array(req.args.get("sources"), ",")  
  if 'search' in req.args:
    search_obj["search"] = req.args.get("search")
  return search_obj