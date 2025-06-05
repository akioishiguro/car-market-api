import awsgi
from flask_restx import Api
from flask import Flask

from services.resources.cars_api_resources import cars_ns
from services.resources.buy_a_new_cars_api_resources import buy_a_new_car_ns

app = Flask(__name__)

api = Api(app)

api.add_namespace(cars_ns)
api.add_namespace(buy_a_new_car_ns)


def api_using_aws_lambda(event, context):
    return awsgi.response(app, event, context)
