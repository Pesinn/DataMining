def conv_req_to_search_obj(req):
  search_obj = {}
  if 'languages' in req.args:
    search_obj["languages"] = req.args.get("languages")
  if 'date_from' in req.args:
    search_obj["date_from"] = req.args.get("date_from")
  if 'date_to' in req.args:
    search_obj["date_to"] = req.args.get("date_to")
  if 'sources' in req.args:
    search_obj["sources"] = req.args.get("sources")
  if 'search' in req.args:
    search_obj["search"] = req.args.get("search")
  
  return search_obj