"""create flask app and define end-points.
host,port and debug arguments could be gotten from system arguments.

"""
import argparse
import logging

from flasgger import Swagger
from flask import Flask
from flask_restful import Api

from api.crawl_api import CrawlAPI

APP = Flask(__name__)
APP.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
APP.config['SWAGGER'] = {
    'title': 'PDF2TILES',
    'uiversion': 3
}
swagger = Swagger(APP)

APP.config.from_object("config.Config")

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    APP.logger.handlers = gunicorn_logger.handlers
    APP.logger.setLevel(gunicorn_logger.level)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s - %(message)s')

LOGGER = logging.getLogger(__name__)

# Swagger(APP)
API = Api(APP)
# add resource to end points
API.add_resource(CrawlAPI, '/api/input_words')

if __name__ == "__main__":
    # create argument host, port, debug mode with default value, and to load from system argument
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--host', type=str, default=APP.config['HOST'])
    PARSER.add_argument('--port', type=int, default=APP.config['PORT'])
    PARSER.add_argument('--debug', type=bool, default=APP.config['DEBUG'])
    ARGS = PARSER.parse_args()
    HOST = ARGS.host
    PORT = ARGS.port
    DEBUG = ARGS.debug
    APP.run(host=HOST, port=PORT, debug=DEBUG)
