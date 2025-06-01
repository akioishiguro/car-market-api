import uuid
import simplejson
from datetime import datetime
from flask import request
from http import HTTPStatus
from flask_restx import Namespace, Resource, fields

from services.repository.dynamodb import DynamoDBRepository

from config import Config
from utils.convert_to_decimal import convert_to_decimal

dynamo_db = DynamoDBRepository(table_name=Config.get('dynamoTableName'), region_name=Config.get('awsRegion'))

cars_ns = Namespace(name='cars', description='Gerenciamento de Carros')

create_car_model = cars_ns.model('Cars', {
    'brand': fields.String(required=True),
    'model': fields.String(required=True),
    'year': fields.Integer(required=True),
    'color': fields.String(required=True),
    'price': fields.Float(required=True),
    'status': fields.String(required=True, enum=['available', 'sold'])
})

response_model = cars_ns.model('Response', {
    'status_success': fields.Boolean,
    'response': fields.Raw,
    'message': fields.String
})


def response_model_helper(status_success: bool, response, message):
    return {
        'status_success': status_success,
        'response': simplejson.dumps(response) if response else None,
        'message': message
    }


@cars_ns.route('/create_car')
class CreateCarResource(Resource):
    # @auth.login_required
    @cars_ns.expect(create_car_model)
    @cars_ns.marshal_with(response_model)
    def post(self):
        data = cars_ns.payload

        data['id'] = str(uuid.uuid4())
        data['create_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        success = dynamo_db.create_item(convert_to_decimal(data))
        if success:
            return response_model_helper(
                status_success=True,
                response=data,
                message='Carro criado com sucesso!'), HTTPStatus.CREATED

        else:
            return response_model_helper(
                status_success=False,
                response=None,
                message='Erro ao criar o carro. Verifique os dados enviados.'
            ), HTTPStatus.BAD_REQUEST


@cars_ns.route('/<string:car_id>')
class CarResource(Resource):
    @cars_ns.marshal_with(response_model)
    def get(self, car_id):
        car = dynamo_db.get_item({'id': car_id})
        if car:
            return response_model_helper(
                status_success=True,
                response=car,
                message='Carro encontrado com sucesso!'
            ), HTTPStatus.OK
        else:
            return response_model_helper(
                status_success=False,
                response=None,
                message='Carro não encontrado.'
            ), HTTPStatus.NOT_FOUND

    @cars_ns.marshal_with(response_model)
    def delete(self, car_id):
        success = dynamo_db.delete_item({'id': car_id})
        if success:
            return response_model_helper(
                status_success=True,
                response=None,
                message='Carro deletado com sucesso!'
            ), HTTPStatus.OK
        else:
            return response_model_helper(
                status_success=False,
                response=None,
                message='Erro ao deletar o carro.'
            ), HTTPStatus.BAD_REQUEST

    @cars_ns.expect(create_car_model)
    @cars_ns.marshal_with(response_model)
    def put(self, car_id):
        data = cars_ns.payload

        success = dynamo_db.update_item(
            key=car_id,
            item=convert_to_decimal(data),
            update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        if success:
            return response_model_helper(
                status_success=True,
                response=data,
                message='Carro atualizado com sucesso!'
            ), HTTPStatus.OK
        else:
            return response_model_helper(
                status_success=False,
                response=None,
                message='Erro ao atualizar o carro. Verifique os dados enviados.'
            ), HTTPStatus.BAD_REQUEST


@cars_ns.route('/get_all_cars')
class CarsListResource(Resource):
    @cars_ns.marshal_with(response_model)
    def get(self):
        cars = dynamo_db.get_all_items()
        if cars:
            cars = sorted(cars, key=lambda row: float(row['price']))
            return response_model_helper(
                status_success=True,
                response=cars,
                message='Lista de carros recuperada com sucesso!'
            ), HTTPStatus.OK
        else:
            return response_model_helper(
                status_success=False,
                response=None,
                message='Nenhum carro encontrado.'
            ), HTTPStatus.NOT_FOUND


@cars_ns.route('/get_all_availables_cars')
class CarsListResource(Resource):
    @cars_ns.marshal_with(response_model)
    def get(self):
        cars = dynamo_db.get_items_by_status('available')
        if cars:
            cars = sorted(cars, key=lambda row: float(row['price']))
            return response_model_helper(
                status_success=True,
                response=cars,
                message='Lista de carros disponiveis para venda recuperada com sucesso!'
            ), HTTPStatus.OK
        else:
            return response_model_helper(
                status_success=False,
                response=None,
                message='Nenhum carro encontrado.'
            ), HTTPStatus.NOT_FOUND


@cars_ns.route('/get_all_sold_cars')
class CarsListResource(Resource):
    @cars_ns.marshal_with(response_model)
    def get(self):
        cars = dynamo_db.get_items_by_status('sold')
        if cars:
            cars = sorted(cars, key=lambda row: float(row['price']))
            return response_model_helper(
                status_success=True,
                response=cars,
                message='Lista de carros ja vendidos recuperada com sucesso!'
            ), HTTPStatus.OK
        else:
            return response_model_helper(
                status_success=False,
                response=None,
                message='Nenhum carro encontrado.'
            ), HTTPStatus.NOT_FOUND
