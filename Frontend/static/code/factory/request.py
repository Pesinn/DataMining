def conv_req_to_query_string(req):
  print(req)
  query_str = ""
  if 'search' in req.args:    
    s = req.args.get("search").split("|")

    # Check if there is no search value
    if(len(s) == 1):
      if(s[0] == ""):
        return "[]"

    query_str += "search=["
    first_run = True
    for i in s:
      print("i: ", i)
      if(first_run == False):
        query_str += ","
      else:
        first_run = False
      query_str += add_object(i)
    query_str += "]"
  return query_str

def add_object(req):
  return "{" + req.strip() + "}"