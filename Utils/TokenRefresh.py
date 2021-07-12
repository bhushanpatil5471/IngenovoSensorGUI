import os
import time
import jwt       # pip install pyjwt==2.1.0
import requests  # pip install requests==2.25.1

# Constants for authentication credentials.
KEY_ID = os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', '')
SECRET = os.environ.get('DT_SERVICE_ACCOUNT_SECRET', '')
EMAIL = os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', '')


class Auth():
    """
    Handles automatic refresh of access token every
    time get_token() is called with a buffer of 1 minute.

    """

    refresh_buffer = 60  # s
    auth_url = 'https://identity.disruptive-technologies.com/oauth2/token'

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

    def get_token(self):
        # Check if access token needs a refresh. A 1 minute buffer is added.
        if self.expiration - time.time() < self.refresh_buffer:
            # Print expiration message to console.
            print('Refreshing...')

            # Fetch a brand new access token and expiration.
            self.refresh()

        # Print time until expiration.
        print('Token expires in {}s.'.format(
            int(self.expiration - time.time() - self.refresh_buffer),
        ))

        # Return the token to user.
        return self.token


def function_that_calls_rest_api(access_token: str):
    # This would usually do something useful.
    time.sleep(5)


if __name__ == '__main__':
    # Initialize an authentication object.
    auth = Auth(KEY_ID, EMAIL, SECRET)

    # Do some task, here simulated by an infinite loop.
    while True:
        # Simulate some routine that needs authentication for the REST API.
        function_that_calls_rest_api(auth.get_token())
