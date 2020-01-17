import logging
from .log import logger

logger.init(__name__)
logger.info("running init of " + __name__)
