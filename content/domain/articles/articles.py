import content.dblayer.dbservice as dbservice

def get_articles(request):
  return dbservice.get_articles()