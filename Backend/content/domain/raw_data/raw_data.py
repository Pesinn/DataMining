import content.dblayer.dbservice as dbservice

def get_raw_data(search, filter):
  return_arr = []
  for i in search:
    return_arr.append(dbservice.get_news_data(i, filter))
  return return_arr