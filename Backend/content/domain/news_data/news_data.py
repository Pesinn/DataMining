import content.dblayer.dbservice as dbservice
import copy

def get_news_data(search):
#  query_list = []
#  if search["search"]:
#    query_obj = {}
#    for i in search["search"]:
#      query_obj = copy.deepcopy(search)
#      query_obj["search"] = i
#      query_list.append(query_obj)

#  return_object = []
#  if search["search"]:
#    for i in search["search"]:
#      return_object.append(dbservice.get_news_data(search))
#  else:
#    return_object.append(dbservice.get_news_data(search))

  return dbservice.get_news_data(search)