import requests
from flask_httpauth import HTTPTokenAuth

from config import Config

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    if token:
        url = "http://localhost:8080/auth/validate_token_by_group"

        payload = 'group_name=clients'
        headers = {
            'Authorization': 'Bearer eyJraWQiOiJtRkY1Q2tZcGNtOHQ3eHZjVmw0NTF0V1czRWtLXC9KV1B2ZW9ZWXVRbmZYST0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzNGY4MjQ0OC1mMDMxLTcwZGUtZWE4Yi1kZDhkN2NiMzExMDciLCJjb2duaXRvOmdyb3VwcyI6WyJjbGllbnRzIl0sImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX3FBVGxqa2ZieiIsImNsaWVudF9pZCI6InUzY3NtdGlsb202cjhyNzB1M21vMTZlNDMiLCJldmVudF9pZCI6Ijg4NjIzYTI2LWFkMWUtNGI1OC05ZTFjLTViMTA4ZDIwMTdjYiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3NDg4MjIwMDUsImV4cCI6MTc0ODgyNTYwNSwiaWF0IjoxNzQ4ODIyMDA1LCJqdGkiOiJlNzZkMTQ5ZC05ZTdiLTRmMzItOGU2NC00YmE5MzY3MTM1YWQiLCJ1c2VybmFtZSI6IjQzNjI5MTI5MDgwIn0.TZrkmJp-a4yl4pswt2AtFR6GEbHS-syksomxfrMwJvhDb_nLpkRjuFRDcJtUEX7rui6rZY1OD7uttt2pBn5XPlvLCAEsDJoKVvGpHuEVr--pfUvEd_Rl2VsulLKki0Gf4_SjKNrbOAW8eCyjSIJqEJ5Eo2mQGw5GCxMZa9wJ0AvGC0Y27dZoFiQ2QXaOtPjFJ21FSTU5m2XGG_XFcAmUU_EYjRPqizqFcgANWcVTh76sPyTSiWWwPeo4-nH4sIwlB0PuHq29nF5Br7qBP8R0HkWAOH4NBI5wMgOWUHgXqUw2yd10INQ6ikvF9ktOIGxUgI2B6MjhlG7UY5UHBDylqQ',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        if response['status_success']:
            return response['message']
