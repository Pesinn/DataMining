def conv_req_to_query_string(req):
  query_str = ""
  query_str = search(query_str, req)
  query_str = search_filter(query_str, req, "articles_limit")
  query_str = search_filter(query_str, req, "articles_range")
  return query_str
  
def search(query_str, req):
  if 'search' in req.args:
    s = req.args.get("search").split("|")

    # Check if there is no search value
    if(len(s) == 1):
      if(s[0] == ""):
        return "[]"

    query_str += "search=["
    first_run = True
    for i in s:
      if(first_run == False):
        query_str += ","
      else:
        first_run = False
      query_str += add_object(i)
    query_str += "]"
  return query_str

def search_filter(query_str, req, name):
  articles_limit = req.args.get(name)
  if articles_limit:
    query_str = add_to_query_str(
      query_str,
      f"{name}={articles_limit}"
    )
  return query_str

def add_to_query_str(query_str, query):
  if query_str in "":
    query_str = query
  else:
    query_str = query_str + "&" + query
  return query_str

def add_object(req):
  return "{" + req.strip() + "}"