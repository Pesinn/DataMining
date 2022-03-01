import static.code.factory.pagination as pagination

def conv_req_to_pre_filter(req):
  filter = {}
  filter["search"] = filter_to_search(req)
  filter["languages"] = pre_filter_array_handler(req, "languages")
  filter["sources"] = pre_filter_array_handler(req, "sources")
  filter["date_from"] = pre_filter_string_handler(req, "date_from")
  filter["date_to"] = pre_filter_string_handler(req, "date_to")
  filter["articles_limit"] = pre_filter_string_handler(req, "articles_limit")
  filter["named_entities"] = pre_filter_string_handler(req, "named_entities")
  filter["articles_range"] = pre_filter_pagination(req, "current_page")
  return filter

def pre_filter_pagination(req, page):
  default = pagination.get_articles_per_page()
  articles_page = req.args.get(page)
  
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

    return {_to, _from}
  return {}

def filter_to_search(req):
  if 'search' in req.args:
    s = req.args.get("search").split("|")

    # Check if there is no search value
    if(len(s) == 1):
      if(s[0] == ""):
        return []
    return s
  return []

def pre_filter_array_handler(req, type):
  value_arr = []  
  val = req.args.get(type)
  if val:
    value_arr = val.split(",")
  return value_arr

def pre_filter_string_handler(req, type):
  return req.args.get(type)

def conv_pre_filter_to_query_string(pre_filter):
  query_str = ""
  for i in pre_filter:
    if i == "search":
      query_str = pre_filter_to_search_query(query_str, pre_filter[i])
    elif pre_filter[i] != None and pre_filter[i] != "" and pre_filter[i] != [] and pre_filter[i] != {}:
      query_str = pre_filter_to_query(query_str, pre_filter, i)
  return query_str

def pre_filter_to_search_query(query_str, elements):
  query_str += "search=["
  first_run = True
  for i in elements:
    if(first_run == False):
      query_str += ","
    else:
      first_run = False
    query_str += add_object(i)
  query_str += "]"
  return query_str

def pre_filter_to_query(query_str, pre_filter, i):
  return add_to_query_str(
    query_str,
    f"{i}={pre_filter[i]}"
  )

def conv_req_to_query_string(req):
  query_str = ""
  query_str = search(query_str, req)
  query_str = search_filter(query_str, req, "articles_limit")
  query_str = search_filter_array(query_str, req, "sources")
  query_str = search_filter_array(query_str, req, "languages")
  query_str = search_filter(query_str, req, "date_from")
  query_str = search_filter(query_str, req, "date_to")
  query_str = search_filter(query_str, req, "named_entities")
  query_str = pagination_handler(query_str, req)

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
  return query_str

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

def pre_filter_to_domain_filter(pre_filter):
  domain_filter = get_default_domain_filter()
  for i in pre_filter:
    activate_domain_filter_attribute(domain_filter, pre_filter[i], i)
  return domain_filter
  
def activate_domain_filter_attribute(domain_filter, element, i):
  if type(element) is str or i == "search":
    domain_filter[i] = element
  elif type(element) is list:
    for e in element:
      domain_filter[i][e] = True

def get_default_domain_filter():
  return {
    "search": [],
    "languages":
    {
      "en": False,
      "fr": False,
      "es": False
    },
    "sources":
    {
      "9news.com.au": False,
      "france24.fr": False,
      "foxnews": False
    },
    "date_from": None,
    "date_to": None,
  }