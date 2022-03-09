import logging

# create logger
logger = logging.getLogger('news_articles.backend')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

def log(data, t):
  d = {
    'DEBUG': lambda: logger.debug(data),
    'INFO': lambda: logger.info(data),
    'WARNING': lambda: logger.warning(data),
    'ERROR': lambda: logger.error(data),
    'CRITICAL': lambda: logger.critical(data),
  }.get(t, lambda: f'Logger: {t} is not a valid type')()
  
  if(d is not None):
    logger.error(d)