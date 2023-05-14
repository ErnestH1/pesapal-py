#!/usr/bin/env python
# coding: utf-8
import base64
import hmac
import hashlib
import jwt
import json
import requests
import time
import uuid
import urllib.parse



class PesaPal(object):
    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.base_production_url = "https://pay.pesapal.com/v3/api"
        self.base_demo_url = "https://cybqa.pesapal.com/pesapalv3/api"
        self.token = ''
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def authenticate(self) -> dict:
        """
        Authenticates against PesaPal

        returns:
            status (str): success or failed (always returned)
            error (str): error message from pesapal when authentication fails (returned only when status is failed)
            message (str): a brief description about the response received (returned only when status is failed)
            token (str): Bearer token to authenticate all other PesaPal APIs (returned only when status is success)
            expiry (str): Date and time the token will expire. The access token usually expires after 5mins - UTC (returned only when status is success)

        Explore https://developer.pesapal.com/how-to-integrate/e-commerce/api-30-json/authentication for more details
        """
        auth_payload = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret,
        }
        auth_response = requests.post(
            f"{self.base_production_url}/Auth/RequestToken",
            json.dumps(auth_payload),
            headers=self.headers,
        )
        if auth_response.status_code == 200:
            auth_data = json.loads(auth_response.content)
            if auth_data["status"] == "200":
                return {
                    "status": "success",
                    "token": auth_data["token"],
                    "expiry": auth_data["expiryDate"],
                }

            else:
                return {
                    "status": "failed",
                    "error": auth_data["error"]["code"],
                    "message": auth_data["error"]["message"],
                }
        return {
            "status": "failed",
            "error": auth_response.status_code,
            "message": f"invalid server response",
        }

    def generate_jwt_signature(self, http_method, endpoint, params, secret_key):
        # Sort parameters alphabetically by key
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        # Concatenate method, endpoint, and sorted parameters
        message = '&'.join([http_method.upper(), endpoint] +
                           [f"{k}={urllib.parse.quote(str(v))}" for k, v in sorted_params])
        # Generate a JWT token for authentication
        jwt_payload = {'username': 'TECH_AIR'}
        jwt_token = jwt.encode(jwt_payload, secret_key, algorithm='HS256')
        # Return the JWT token as the signature
        print('JWT_Token = {}'.format(jwt_token))
        return jwt_token

    def build_signature(self, request, consumer, params, token):
        pesapal_url = "https://www.pesapal.com/API/PostPesapalDirectOrderV4"
        signature_base_string = f"POST&{urllib.parse.quote(pesapal_url, safe = '')}&{urllib.parse.quote(params, safe='')}"
        base_string = signature_base_string

        key_parts = [
            self.consumer_secret,
            token if token else ""
        ]

        key_parts = list(map(urllib.parse.quote, key_parts))
        key = '&'.join(key_parts).encode('utf-8')

        message = base_string.encode('utf-8')
        signature = hmac.new(key, message, hashlib.sha1).digest()
        signature = base64.b64encode(signature).decode('utf-8')

        return signature

    def get_iframe(self, token: str) -> dict:
        JWT_SECRET_KEY = self.consumer_secret
        timestamp = int(time.time())
        print('Timestamp = {}'.format(timestamp))

        # Generate a JWT token for authentication
        jwt_payload = {'username': 'TECH_AIR'}
        jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY,
                               algorithm='HS256')

        pesapal_url = "https://www.pesapal.com/API/PostPesapalDirectOrderV4"
        params = {
            'oauth_consumer_key': self.consumer_key,
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_signature': jwt_token,
            'oauth_timestamp': str(timestamp),
            'oauth_nonce': '0ni4v40flbujac1',
            'pesapal_request_data': '<PesapalDirectOrderInfo xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><Amount>100</Amount><Currency>UGX</Currency><Description>Test Order</Description><Type>MERCHANT</Type><Reference>1</Reference><FirstName>John</FirstName><LastName>Doe</LastName><Email>test@example.com</Email><PhoneNumber></PhoneNumber><LineItems></LineItems><CallbackURL></CallbackURL></PesapalDirectOrderInfo>'
        }
        sorted_params = "&".join(
            [f"{k}={v}" for k, v in sorted(params.items())])

        signature = self.generate_jwt_signature(
            'POST', 'https://www.pesapal.com/API/PostPesapalDirectOrderV4', params, 'your_consumer_secret')

        sign = self.build_signature('<PesapalDirectOrderInfo xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><Amount>100</Amount><Currency>UGX</Currency><Description>Test Order</Description><Type>MERCHANT</Type><Reference>1</Reference><FirstName>John</FirstName><LastName>Doe</LastName><Email>test@example.com</Email><PhoneNumber></PhoneNumber><LineItems></LineItems><CallbackURL></CallbackURL></PesapalDirectOrderInfo>',
                                    {'key': self.consumer_key, 'secret': self.consumer_secret}, sorted_params, token)

        params['oauth_signature'] = sign

        response = requests.get(pesapal_url, params=params)

        print(response.content)


pesapal = PesaPal("qVsdDrEN6iVqHaHzQHiBR0Kyavw5wVQl",
                  "gJiE7pWglYLfIA7TprswlRw8Ws0=")
auth = pesapal.authenticate()
mytoken = str(auth['token'])
print(mytoken)
myiframe = pesapal.get_iframe(mytoken)
print(myiframe)