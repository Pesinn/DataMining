import content.dblayer.dbservice as dbservice

def get_raw_data(search):
  return_arr = []
  for i in search:
    return_arr.append(dbservice.get_raw_data(i))
  return return_arr