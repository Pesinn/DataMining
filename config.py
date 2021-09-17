ENV = "TEST"

DB_COLLECTION = {}
DB_COLLECTION["TEST"] = "articles_TEST"
DB_COLLECTION["PROD"] = "articles"
DB_COLLECTION["DEV"] = "None"

def get_db_collection():
  return DB_COLLECTION[ENV]

DB_HOST = "localhost"
DB_PORT = 27017