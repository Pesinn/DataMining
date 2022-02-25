import static.code.factory.pagination as pagination

def conv_req_to_query_string(req):
  filter = {}
  print(req)
  query_str = ""
  query_str = search(query_str, req)
  query_str = search_filter(query_str, req, "articles_limit")
  query_str, filter["sources"] = search_filter_array(query_str, req, "sources")
  query_str, filter["languages"] = search_filter_array(query_str, req, "languages")
  query_str = search_filter(query_str, req, "named_entities")
  query_str = pagination_handler(query_str, req)

  print("languages", filter["languages"])

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
  val = req.args.get(name)
  if val:
    query_str = add_to_query_str(
      query_str,
      f"{name}={val}"
    )
  return query_str

def search_filter_array(query_str, req, name):
  value_arr = []
  val = req.args.get(name)
  if val:
    value_arr = val.split(",")
    query_str = add_to_query_str(
      query_str,
      f"{name}={value_arr}"
    )
  return query_str, value_arr

def add_to_query_str(query_str, query):
  if query_str in "":
    query_str = query
  else:
    query_str = query_str + "&" + query
  return query_str

def add_object(req):
  return "{" + req.strip() + "}"

def pagination_handler(query_str, req):
  default = pagination.get_articles_per_page()
  articles_page = req.args.get("current_page")
    
  # Page 1: 1,10
  # Page 2: 11,20
  # Page 3: 21,30
  # Page 4: 31,40
  # Page 5: 41,50
  if articles_page:
    articles_page = int(articles_page)
    if articles_page < 1:
      articles_page = 1
    if(articles_page == 1):
      _from = 1
      _to = default
    else:
      _from = default*(articles_page-1) + 1
      _to = default*articles_page
      
    query_str = add_to_query_str(
      query_str,
      f"articles_range={_from},{_to}"
    )

  return query_str