from matplotlib import image
import multidict as multidict
import numpy as np
import random

from PIL import Image
from wordcloud import WordCloud

generated_image_path = "static/generated_images/"

image_data = {
  'default':
  {
    'img': 'static/images/default_mask.png',
    'background_color': 'white',
    'contour_width': 3,
    'contour_color': 'black',
    'ui_height': '400px'
  },
  'alice_1':
  {
    'img': 'static/images/alice_mask.png',
    'background_color': 'pink',
    'contour_width': 2,
    'contour_color': 'black',
    'ui_height': '600px'
  },
  'alice_2':
  {
    'img': 'static/images/alice_mask.png',
    'background_color': 'white',
    'contour_width': 3,
    'contour_color': 'steelblue',
    'ui_height': '600px'
  },
  'alice_3':
  {
    'img': 'static/images/alice_mask.png',
    'background_color': 'white',
    'contour_width': 0,
    'contour_color': 'steelblue',
    'ui_height': '600px'
  },
  'stormtrooper_1':
  {
    'img': 'static/images/stormtrooper_mask.png',
    'background_color': 'grey',
    'contour_width': 3,
    'contour_color': 'white',
    'ui_height': '600px'
  },
  'stormtrooper_2':
  {
    'img': 'static/images/stormtrooper_mask.png',
    'background_color': 'white',
    'contour_width': 5,
    'contour_color': 'black',
    'ui_height': '600px'
  },
  'stormtrooper_3':
  {
    'img': 'static/images/stormtrooper_mask.png',
    'background_color': 'white',
    'contour_width': 0,
    'contour_color': 'black',
    'ui_height': '600px'
  }
}

def create_word_clouds(ent):
  image_freq = getFrequencyDictForText(ent[0]["entities"]["named"])
  out_img_arr = []

  for i in image_data:
    wc = create_word_cloud(i)
    wc.generate_from_frequencies(image_freq)
    random_str = random_string()
    wc.to_file(f"{generated_image_path}{random_str}.png")
    out_img_arr.append(
      {
        'path': f"{generated_image_path}{random_str}.png",
        'height': image_data[i]["ui_height"]
      }
    )
  
  return out_img_arr

def create_word_cloud(image):
  img = image_data[image]
  arr = np.array(Image.open(img["img"]))
  wc = WordCloud(
    background_color=img["background_color"],
    mask=arr,
    contour_width=img["contour_width"],
    contour_color=img["contour_color"]
  )
  return wc

def getFrequencyDictForText(sentence):
  dict = multidict.MultiDict()
  for s in sentence:
    dict.add(s["entity"], s["count"])
  return dict

def random_string(random_chars=12, alphabet="0123456789abcdef"):
    r = random.SystemRandom()
    return ''.join([r.choice(alphabet) for i in range(random_chars)])