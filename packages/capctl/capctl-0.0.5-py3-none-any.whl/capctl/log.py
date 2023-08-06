import os
import coloredlogs
import logging
import logging.config

# export COLOREDLOGS_LOG_FORMAT='%(asctime)s %(levelname)7s (%(filename)16s:%(lineno)4s): %(message)s'
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logger = logging.getLogger()
coloredlogs.install(level=LOGLEVEL, logger=logger)
