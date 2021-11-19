import content.dblayer.dbservice as dbservice
import content.domain.sentiment.sentiment_analysis as sentiment
import content.domain.sentiment.sentiment_analysis_factory as sentiment_factory

def get_news_data(search):
  return_arr = []
  for i in search:
    s_analysis = []
    data = dbservice.get_news_data(i)
    articles = []
    for d in data:
      article = {
        "title": d["title"]["text"],
        "description": d["description"]["text"],
        "language": d["article_language"],
        "source": d["source"],
        "publish_date": d["publish_date"],
      }
      articles.append(article)
    final_obj = {
      "sentiment_analysis": sentiment_factory.convert_db_data_to_domain_data_obj(data, i["search"][0])["sentiment_analysis"],
      "articles": articles,
      "search": i["search"][0]
    }
    return_arr.append(final_obj)

  return return_arr