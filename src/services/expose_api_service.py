from flask import Flask
from waitress import serve
from flask_restx import Api

from services.resources.cars_api_resources import cars_ns

app = Flask(__name__)


class ApiService(object):
    HOST = '0.0.0.0'
    PORT = 8080

    def __init__(self):
        self.api = Api(app,
                       version='1.0',
                       title='API',
                       description='Cars Market API',
                       doc='/swagger/')

    def run(self):
        self.api.add_namespace(cars_ns)
        print('Serving on http://localhost:{}/swagger/'.format( self.PORT))
        serve(app, host=self.HOST, port=self.PORT)