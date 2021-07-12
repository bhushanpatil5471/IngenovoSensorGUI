import os
import time
import jwt
import requests
from Constants import KeyEmails

# Authentication details used in the OAuth2 flow.


# SERVICE_ACCOUNT_KEY_ID = os.environ.get('SERVICE_ACCOUNT_KEY_ID','c3dfdtb531lg009b6bng')
# SERVICE_ACCOUNT_SECRET = os.environ.get('SERVICE_ACCOUNT_SECRET','665df80c49544406974a9a3d7905d351')
# SERVICE_ACCOUNT_EMAIL = os.environ.get('SERVICE_ACCOUNT_EMAIL','c3dfdl49sk8000d74u60@c39ghc9m4b6ce48o0e50.serviceaccount.d21s.com')


def get_access_token():
    # Construct the JWT header.
    SERVICE_ACCOUNT_KEY_ID = KeyEmails.SERVICE_ACCOUNT_KEY_ID
    SERVICE_ACCOUNT_SECRET = KeyEmails.SERVICE_ACCOUNT_SECRET
    SERVICE_ACCOUNT_EMAIL = KeyEmails.SERVICE_ACCOUNT_EMAIL

    jwt_headers = {
        'alg': 'HS256',
        'kid': SERVICE_ACCOUNT_KEY_ID,
    }

    # Construct the JWT payload.
    jwt_payload = {
        'iat': int(time.time()),         # current unixtime
        'exp': int(time.time()) + 3600,  # expiration unixtime
        'aud': 'https://identity.disruptive-technologies.com/oauth2/token',
        'iss': SERVICE_ACCOUNT_EMAIL,
    }

    # Sign and encode JWT with the secret.
    encoded_jwt = jwt.encode(
        payload=jwt_payload,
        key=SERVICE_ACCOUNT_SECRET,
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
        url='https://identity.disruptive-technologies.com/oauth2/token',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data=request_data,
    )

    # Halt if response contains an error.
    if access_token_response.status_code != 200:
        print('Status Code: {}'.format(access_token_response.status_code))
        print(access_token_response.json())
        return None

    # Return the access token in the request.
    return access_token_response.json()['access_token']


def main():
    # Get an access token using an OAuth2 authentication flow.
    access_token = get_access_token()

    # Verify that we got a valid token back.

    if access_token is None:
        return "error"+ access_token

    print(access_token)
    # print('access token'+ access_token)
    # Test the token by sending a GET request for a list of projects.
    # print(requests.get(
    #     url='https://api.disruptive-technologies.com/v2/projects',
    #     headers={'Authorization': 'Bearer ' + access_token},
    # ).json())


if __name__ == '__main__':
    main()
