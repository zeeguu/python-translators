import logging

logger = logging.getLogger('python_translators')
logger.setLevel(logging.DEBUG)

# General logging tracking ALL logs
fh = logging.FileHandler('translators.log', encoding = "UTF-8")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)


fh2 = logging.FileHandler('errors.translators.log')
fh2.setLevel(logging.ERROR)
fh2.setFormatter(formatter)

logger.addHandler(fh2)
logger.addHandler(fh)

logger.info('Logger initialized.')
