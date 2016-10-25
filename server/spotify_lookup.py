import base64

import requests

import auth


def get_playlists(user_id):
    """Return list of playlists for this user."""
    auth_token = get_auth_token()
    auth_string = 'Bearer {}'.format(auth_token)

    endpoint = 'https://api.spotify.com/v1/users/{}/playlists'.format(user_id)
    header = {'Authorization': auth_string}

    return requests.get(endpoint, headers=header)


def get_auth_token():
    """Return authentication token generated using client credentials flow.

    This authentication method does not give access to user data endpoints.
    """
    endpoint = 'https://accounts.spotify.com/api/token'
    header = build_auth_header()
    payload = {'grant_type': 'client_credentials'}

    response = requests.post(endpoint, headers=header, data=payload)

    return response.json()['access_token']


def spotify_auth_request():
    """Request user authentication with spotify"""
    endpoint = 'https://accounts.spotify.com/authorize'
    payload = {'client_id': auth.SPOTIFY_CLIENT_ID,
               'response_type': 'code',
               'scope': 'user-library-read user-top-read',
               'redirect_uri': 'http://localhost:5000/authcallback'}

    return requests.get(endpoint, params=payload)


def swap_auth_code_for_token(auth_code):
    """Swap the authenticated user code for an access token."""
    endpoint = 'https://accounts.spotify.com/api/token'
    header = build_auth_header()
    # content type needs to be set because of a bug?
    # see https://github.com/spotify/web-api/issues/190
    header['Content-Type'] = 'application/x-www-form-urlencoded'

    payload = {'grant_type': 'authorization_code',
               'code': auth_code,
               'redirect_uri': 'http://localhost:5000/authcallback'}

    response = requests.post(endpoint, headers=header, params=payload)

    return response.json()['access_token']


def build_auth_header():
    tokens = '{}:{}'.format(auth.SPOTIFY_CLIENT_ID, auth.SPOTIFY_TOKEN)
    encoded = base64.b64encode(tokens.encode())
    auth_string = 'Basic {}'.format(encoded.decode())
    return {'Authorization': auth_string}


def get_saved_tracks(user_token):
    """Return all starred tracks for authenticated user."""
    auth_string = 'Bearer {}'.format(user_token)

    endpoint = 'https://api.spotify.com/v1/me/tracks'
    header = {'Authorization': auth_string}
    payload = {'limit': 200}

    response = requests.get(endpoint, headers=header, params=payload)
    import ipdb; ipdb.set_trace()

    return response


if __name__ == '__main__':
    get_playlists()
