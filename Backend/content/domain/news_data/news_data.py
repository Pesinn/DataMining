import content.dblayer.dbservice as dbservice
import content.domain.sentiment.sentiment_analysis as sentiment
import content.domain.sentiment.sentiment_analysis_factory as factory

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

#  for i in search:
#    data = dbservice.get_news_data(search)
    

#  sentiment = []
#  for i in data:
#    sentiment.append(i["annotations"])
#  for i in data:
 #   print(i)
  #  print(" ")

#  print(sentiment)

  #res = sentiment.get_sentiment_analysis_from_db(search)
  return_arr = []

  for i in search:
    s_analysis = []
    data = dbservice.get_news_data(i)
    articles = []
    for d in data:
      article = {
        "title": d["title"]["text"],
        "description": d["description"]["text"],
        "language": d["language"],
        "source": d["source"],
        "publish_date": d["publish_date"]
      }
      articles.append(article)
    s_analysis.append(factory.convert_db_data_to_domain_data_obj(data, i["search"][0]))
    final_obj = {
      "sentiment_analysis": s_analysis[0]["sentiment_analysis"],
      "articles": articles,
      "search": i["search"][0]
    }
    return_arr.append(final_obj)

#  sentiment = []
#  for i in data:
#    sentiment.append(i["annotations"])


    


  #for i in res:
  # print(i)
  #  print("")

  return return_arr