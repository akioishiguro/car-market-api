# from services.expose_api_aws import api_using_aws_lambda
from services.expose_api_service import ApiService

# def lambda_handler(event, context):
#     try:
#         logger.info('Lambda handler started!!')
#         logger.info(event)
#         return api_using_aws_lambda(event, context)
#     except Exception as e:
#         logger.error(f'Unhandled exception: {e}')
#         raise e

if __name__ == '__main__':
    ApiService().run()