import multidict as multidict
import numpy as np
import random

from PIL import Image
from wordcloud import WordCloud

generated_image_path = "static/generated_images/"

images = {
  'alice': 'static/images/alice_mask.png',
  'stormtrooper': 'static/images/stormtrooper_mask.png',
  'default': 'static/images/default_mask.png',
}

def create_word_cloud(ent):
  image_freq = getFrequencyDictForText(ent[0]["entities"]["named"])

  wc = create_alice_word_cloud(ent)
  
  wc.generate_from_frequencies(image_freq)

  random_str = random_string()
  wc.to_file(f"{generated_image_path}{random_str}.png")
  
  return f"{generated_image_path}{random_str}.png"

def create_alice_word_cloud(ent):
  arr = np.array(Image.open(images["alice"]))
  wc = WordCloud(
    background_color="white",
    mask=arr
#    contour_width=3,
#    contour_color='steelblue'
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