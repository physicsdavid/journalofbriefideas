from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth

import flask_oauthlib.client
orig_make_request = flask_oauthlib.client.make_request

from figshare_credentials import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
)

ACCESS_TOKEN_URL = 'http://api.figshare.com/v1/pbl/oauth/access_token'

def patched_make_request(uri, headers=None, data=None, method=None, test_client=None):
    '''
    Monkeypatch HTTP method for access_token_url (defaults to GET with no way to override).
    '''
    if uri == ACCESS_TOKEN_URL:
        method = "POST"
    return orig_make_request(uri, headers, data, method, test_client)
flask_oauthlib.client.make_request = patched_make_request

## setup #######################################################################

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

figshare = oauth.remote_app(
    'figshare',
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    request_token_params={'scope': ''},
    base_url='https://api.figshare.com/v1/',
    request_token_url='http://api.figshare.com/v1/pbl/oauth/request_token',
    access_token_method='POST', #XXX does not work with oauth1? see monkeypatch above
    access_token_url=ACCESS_TOKEN_URL,
    authorize_url='http://api.figshare.com/v1/pbl/oauth/authorize',
)

## app #########################################################################

@app.route('/')
def index():
    if 'figshare_token' in session:
        return jsonify(figshare.get('/my_data/articles'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return figshare.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('figshare_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
@figshare.authorized_handler
def authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['figshare_token'] = (resp['oauth_token'], '')
    #other stuff in resp:
    #{'oauth_token_secret': u'1NjTzzzzzzzzzzzzzzzzzz',
    # 'oauth_token': u'J4is8Yxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    # 'xoauth_figshare_id': u'4nnnnnn'
    #}
    return jsonify({'ok': 1})

@figshare.tokengetter
def get_figshare_oauth_token():
    return session.get('figshare_token')

if __name__ == '__main__':
    app.run(port=80)
