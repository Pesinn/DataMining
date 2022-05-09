def get_total_articles_count(data):
  total_article_count = 0
  for i in data:
    total_article_count += i["articles_count"]["total"]
  return total_article_count