import boto3
from flask import request
from http import HTTPStatus
from flask_restx import Namespace, Resource, fields
import uuid

from config import Config

cars_ns = Namespace(name='cars', description='Gerenciamento de Carros')

create_car_model = cars_ns.model('Veiculo', {
    'id': fields.String(readOnly=True),
    'brand': fields.String(required=True),
    'model': fields.String(required=True),
    'year': fields.Integer(required=True),
    'color': fields.String(required=True),
    'price': fields.Float(required=True)
})

response_model = cars_ns.model('Response', {
    'status_success': fields.Boolean,
    'response': fields.Raw,
    'message': fields.String
})

@cars_ns.route('/create_user')
class CreateUserResource(Resource):
    # @auth.login_required
    @cars_ns.expect(create_car_model)
    @cars_ns.marshal_with(response_model)
    def post(self):
        if True:
            return HTTPStatus.CREATED
        else:
            return HTTPStatus.BAD_REQUEST