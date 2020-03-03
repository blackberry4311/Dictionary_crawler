""" DeltaLake API resource for flask endpoints
Each endpoint has a resource class
"""
import json
import logging

from flask import request, Response
from flask_restful import Resource

from services.crawl_service import CrawlService

LOGGER = logging.getLogger(__name__)


class CrawlAPI(Resource):
    """
    """

    def __init__(self):
        self.service = CrawlService()

    def post(self):
        """
        pass a list of words to crawler, crawl at cambridge and saved to MongoDB ODS
        ---
        consumes:
        - application/json
        produces:
        - application/json
        parameters:
        - name: words
          in: body
          description: list of words would pass to scrapy to crawl
          required: true
          schema:
            type: array
            items:
              type: string

        responses:
          202:
            description: ACCEPTED
          405:
            description: invalid input
        """
        request_body = json.loads(request.data)
        self.service.craw_word_list(request_body)

        return Response(None, status=202, mimetype='application/json')
