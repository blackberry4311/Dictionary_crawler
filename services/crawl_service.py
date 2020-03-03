""" DeltaLake API resource for flask endpoints
Each endpoint has a resource class
"""
import logging
import os

from flask import current_app

LOGGER = logging.getLogger(__name__)


class CrawlService:
    """
    """

    def __init__(self):
        upload_location = current_app.config.get('UPLOAD_LOCATION')
        if not os.path.exists(upload_location):
            os.mkdir(upload_location)
        self.upload_location = upload_location

    def craw_word_list(self, request):
        LOGGER.debug(request)
        return request
