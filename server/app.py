from flask import Flask, request, redirect

import spotify_lookup

app = Flask(__name__)


@app.route('/')
def oi_oi():
    return 'MELLIFLUOUS!'


@app.route('/login')
def authenticate():
    print('Requesting spotify user login')
    response = spotify_lookup.spotify_auth_request()

    if response.status_code != 200:
        print('---- REQUEST URL: {}'.format(response.url))
        print('---- ERROR: {}'.format(response.text))
        response.raise_for_status()

    return redirect(response.url)


@app.route('/authcallback')
def store_token():
    error = request.args.get('error')
    if error:
        raise Exception(error)
    auth_code = request.args.get('code')
    print('------ AUTH CODE: {}'.format(auth_code))
    return 'CALLBACK'


if __name__ == '__main__':
    app.run(debug=True)
