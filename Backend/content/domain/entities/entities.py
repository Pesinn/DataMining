import content.dblayer.dbservice as dbservice
import copy

def get_entities(search):
  s = split_query_by_search_keyword(search)

  entities = []
  for i in s["search"]:
    entities.append(dbservice.get_news_data(i))

  return ""

def split_query_by_search_keyword(search):
  query_list = []
  if search["search"]:
    query_obj = {}
    for i in search["search"]:
      query_obj = copy.deepcopy(search)
      query_obj["search"] = []
      query_obj["search"].append(i)
      query_list.append(query_obj)
  return query_list