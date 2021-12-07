import math
import numpy as np

def article_pagination(response, request):
  current_page = request.args.get("current_page")
  if(current_page is None):
    current_page = 1

  per_page = 10
  article_count = response["articles_count_total"]
  pages = math.ceil(article_count / per_page)
  
  r = {
    "pages_count": pages,
    "pages": [
    ]
  }

  # Array of pages that should be visible in the pagination.
  pagination_visible = get_pagination_to_display(int(current_page), int(pages))
    
  # Create object for each page, that contains all key information about
  # what should be displayed.
  for i in range(pages):
    if(i == 0):
      _from = 1
    else:
      _from = (i*10) + 1

    to = 10*(i+1)
    if(to > article_count):
      to = article_count

    number = i+1

    visible = 0
    if (i+1 in pagination_visible):
      visible = 1

    r["pages"].append({
        "page": number,
        "from": _from,
        "to": to,
        "visible": visible
      })

  return r

def get_pagination_to_display(current, pages):
  if(pages < 7 or current > pages or current < 0):
    return [i for i in range(pages)]

  pagination = [current]
  pagination_cap = False
    
  index = 1
  while not pagination_cap:
    left = current - index

    if(left > 0):
      pagination.append(left)
    right = current + index

    if(right <= pages):
      pagination.append(right)
    index += 1
    
    if(len(pagination) >= 7):
      pagination_cap = True
 
  return np.sort(np.array(pagination))
    