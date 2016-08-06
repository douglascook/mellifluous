import base64

import requests

import auth


def get_token():
    """Return authentication token generated using client credentials flow."""
    endpoint = 'https://accounts.spotify.com/api/token'
    payload = {'grant_type': 'client_credentials'}

    auth_string = '{}:{}'.format(auth.SPOTIFY_CLIENT_ID, auth.SPOTIFY_TOKEN)
    auth_encoded = base64.b64encode(auth_string.encode())
    header = {'Authorization': 'Basic {}'.format(auth_encoded.decode())}

    response = requests.post(endpoint, headers=header, data=payload)

    return response.json()['access_token']


if __name__ == '__main__':
    token = get_token()
