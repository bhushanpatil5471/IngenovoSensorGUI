import os
import time
import jwt       # pip install pyjwt==2.1.0
import requests  # pip install requests==2.25.1
from Constants import KeyEmails,Constants
from Utils import NewAccessToken as accessTkn

# Constants for authentication credentials.
KEY_ID = KeyEmails.SERVICE_ACCOUNT_KEY_ID
SECRET = KeyEmails.SERVICE_ACCOUNT_SECRET
EMAIL = KeyEmails.SERVICE_ACCOUNT_EMAIL


class Auth:
    auth_url = Constants.refresh_token_url

    def __init__(self, key_id: str, email: str, secret: str):
        # Set attributes.
        self.key_id = key_id
        self.email = email
        self.secret = secret

        # Initialize some variables.
        self.token = ''
        self.expiration = 0

    def refresh(self):
        # Construct the JWT header.
        jwt_headers = {
            'alg': 'HS256',
            'kid': self.key_id,
        }

        # Construct the JWT payload.
        jwt_payload = {
            'iat': int(time.time()),         # current unixtime
            'exp': int(time.time()) + 3600,  # expiration unixtime
            'aud': self.auth_url,
            'iss': self.email,
        }

        # Sign and encode JWT with the secret.
        encoded_jwt = jwt.encode(
            payload=jwt_payload,
            key=self.secret,
            algorithm='HS256',
            headers=jwt_headers,
        )

        # Prepare HTTP POST request data.
        # note: The requests package applies Form URL-Encoding by default.
        request_data = {
            'assertion': encoded_jwt,
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer'
        }

        # Exchange the JWT for an access token.
        access_token_response = requests.post(
            url=self.auth_url,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=request_data,
        )

        # Halt if response contains an error.
        if access_token_response.status_code != 200:
            print('Status Code: {}'.format(access_token_response.status_code))
            print(access_token_response.json())
            return None

        # Unpack the response dictionary.
        token_json = access_token_response.json()
        self.token = token_json['access_token']
        self.expiration = time.time() + token_json['expires_in']

        if self.expiration < 60:
            return accessTkn.get_access_token()
        else:
            return self.token

