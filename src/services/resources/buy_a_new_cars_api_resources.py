import uuid
import simplejson
from http import HTTPStatus
from datetime import datetime
from flask_restx import Namespace, Resource, fields

from config import Config
from utils.convert_to_decimal import convert_to_decimal
from services.repository.dynamodb import DynamoDBRepository

dynamo_db = DynamoDBRepository(table_name=Config.get('dynamoTableName'), region_name=Config.get('awsRegion'))

buy_a_new_car_ns = Namespace(name='buy_a_new_car', description='Gerenciamento de Carros')

create_car_model = buy_a_new_car_ns.model('Cars', {
    'status': fields.String(required=True, enum=['sold'])
})

response_model = buy_a_new_car_ns.model('Response', {
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


@buy_a_new_car_ns.route('/<string:car_id>')
class CarResource(Resource):
    @buy_a_new_car_ns.expect(create_car_model)
    @buy_a_new_car_ns.marshal_with(response_model)
    def put(self, car_id):
        data = buy_a_new_car_ns.payload

        if data.get('status') != 'sold':
            return response_model_helper(
                status_success=False,
                response=None,
                message='Status inválido.'
            ), HTTPStatus.BAD_REQUEST

        get_car = dynamo_db.get_item(key={'id': car_id})

        if get_car is None or get_car.get('status') == 'sold':
            return response_model_helper(
                status_success=False,
                response=None,
                message='Carro não encontrado ou já vendido.'
            ), HTTPStatus.BAD_REQUEST

        get_car['status'] = 'sold'

        success = dynamo_db.update_item(
            key=car_id,
            item=convert_to_decimal(get_car),
            update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        if success:
            return response_model_helper(
                status_success=True,
                response=get_car,
                message='Carro comprado com sucesso!'
            ), HTTPStatus.OK
        else:
            return response_model_helper(
                status_success=False,
                response=None,
                message='Erro ao finalizar a compra do carro. Verifique os dados enviados.'
            ), HTTPStatus.BAD_REQUEST
