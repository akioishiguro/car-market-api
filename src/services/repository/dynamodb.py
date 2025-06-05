import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key


class DynamoDBRepository:
    def __init__(self, table_name, region_name):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def create_item(self, item):
        try:
            self.table.put_item(Item=item)
            return True
        except ClientError as e:
            print(e.response['Error']['Message'])
            return False

    def get_item(self, key):
        try:
            response = self.table.get_item(Key=key)
            return response.get('Item')
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None

    def update_item(self, key, item, update_at):
        try:
            if key is None:
                raise ValueError("Key cannot be None")

            item['id'] = key
            item['updated_at'] = update_at

            self.table.put_item(Item=item)
            print('ok')
            return True
        except ClientError as e:
            print(e.response['Error']['Message'])
            return False

    def delete_item(self, key):
        try:
            self.table.delete_item(Key=key)
            return True
        except ClientError as e:
            print(e.response['Error']['Message'])
            return False

    def get_all_items(self):
        try:
            items = []
            response = self.table.scan()
            items.extend(response.get('Items', []))

            while 'LastEvaluatedKey' in response:
                response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items.extend(response.get('Items', []))

            return items
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None

    def get_items_by_status(self, status):
        try:
            response = self.table.query(
                IndexName='status-index',
                KeyConditionExpression=Key('status').eq(status)
            )
            return response.get('Items', [])
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None
