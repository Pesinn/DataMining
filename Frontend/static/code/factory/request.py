def conv_req_to_query_string(req):
  query_str = ""
  if 'search' in req.args:
    s = req.args.get("search").split("|")
    query_str += "search=["
    first_run = True
    for i in s:
      if(first_run == False):
        query_str += ","
      else:
        first_run = False
      query_str += i.strip()
    query_str += "]"
  return query_str