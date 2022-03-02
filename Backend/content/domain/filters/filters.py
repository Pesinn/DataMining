import content.dblayer.dbservice as dbservice

def get_filters():
  languages = dbservice.get_filters("article_language")
  sources = dbservice.get_filters("source")
  return {
    "languages": languages,
    "sources": sources
  }