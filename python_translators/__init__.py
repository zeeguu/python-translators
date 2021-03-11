import logging
import sys

logger = logging.getLogger("python_translators")
logger.setLevel(logging.DEBUG)

# General logging tracking ALL logs
# to log to file use the following line
# fh = logging.FileHandler('translators.log', encoding = "UTF-8")
fh = logging.StreamHandler(sys.stdout)

fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)


# use the following line for logging to file
# fh2 = logging.FileHandler("errors.translators.log")
fh2 = logging.StreamHandler(sys.stdout)

fh2.setLevel(logging.ERROR)
fh2.setFormatter(formatter)

logger.addHandler(fh2)
logger.addHandler(fh)

logger.info("Logger initialized.")
