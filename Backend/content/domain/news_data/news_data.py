import content.dblayer.dbservice as dbservice
import content.domain.sentiment.sentiment_analysis as sentiment
import content.domain.sentiment.sentiment_analysis_factory as sentiment_factory
import content.domain.entities.entities_factory as entity_factory

"""
filter = {
  named_entities: true,
  sentiment_analysis: true,
  articles: {
    limit: 20,
    orderby: date
  }
}
"""
def get_news_data(search, filter):
  return_arr = []
  for i in search:
    return_arr.append(get_news_data_by_single_search(i, filter))
  return return_arr

def get_news_data_by_single_search(s, filter):
  data = dbservice.get_news_data(s)
  articles = []
  limit = 10
  index = 0
  sentiment = {}
  ner = {}
  
  for d in data:
    index += 1
#    print(d["annotations"]["entities"]["named"])
    sentiment = sentiment_factory.calculate_score(
      sentiment, d["annotations"]["sentiment_analysis"])
    ner = entity_factory.count_entities(
      ner, d["annotations"]["entities"]["named"])
    
    if index <= limit:
      articles.append(create_article(d))
  
  final_obj = {
    "sentiment_analysis": sentiment,
    "entities": {"named": ner },
    "articles": articles,
    "search": s["search"][0]
  }
  return final_obj

def create_article(data):
  return {
    "title": data["title"]["text"],
    "description": data["description"]["text"],
    "language": data["article_language"],
    "source": data["source"],
    "publish_date": data["publish_date"]
  }