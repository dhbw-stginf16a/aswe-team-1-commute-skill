#!/usr/bin/env python3
import logging
import threading
import time

import requests
from requests.exceptions import ConnectionError

logger = logging.getLogger(__name__)


class RegistrationThread:

    def __init__(self, centralNode, ownURL):
        self.run = True
        self.CENTRAL_NODE_BASE_URL = centralNode
        self.OUR_URL = ownURL

    def start(self):
        logger.info('Starting registration thread')
        thread = threading.Thread(target=self.register)
        thread.start()
        return thread

    def register(self):
        while self.run:
            logger.info("Attempt registration")
            try:
                r = requests.post("{}/skill".format(self.CENTRAL_NODE_BASE_URL), json = { "name": "commute", "endpoint": self.OUR_URL, "interests": ["time"]})  # TODO add more interests
                if r.status_code == 204:
                    logger.info("Registered")
                    self.run = False
                    break
            except ConnectionError as conn:
                logger.warning('Attempted registration failed: %s', conn)
                logger.warning('Retrying in 5 seconds')

            time.sleep(5)

    def stop(self):
        self.run = False