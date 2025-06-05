import requests
from flask_httpauth import HTTPTokenAuth

from config import Config

auth = HTTPTokenAuth(scheme='Bearer')

url = Config.get('authUrl')

ADMIN_GROUP_NAME= 'admin'

@auth.verify_token
def verify_token(token):
    if token:
        if token.startswith('Bearer '):
            token = token[len('Bearer '):]

        payload = f'group_name={ADMIN_GROUP_NAME}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()

        if response['status_success']:
            return response['message']
