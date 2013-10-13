from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from flask_oauthlib.client import OAuth

import flask_oauthlib.client
orig_make_request = flask_oauthlib.client.make_request

import requests

from figshare_credentials import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
)
from figshare_api import FigshareClient, get_name_from_figshare_id

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
    base_url='http://api.figshare.com/v1/',
    request_token_url='http://api.figshare.com/v1/pbl/oauth/request_token',
    access_token_method='POST', #XXX does not work with oauth1? see monkeypatch above
    access_token_url=ACCESS_TOKEN_URL,
    authorize_url='http://api.figshare.com/v1/pbl/oauth/authorize',
)

## app #########################################################################

@app.route('/')
def index():
    client = FigshareClient(access_token, access_token_secret)
    big_ideas = client.get_big_ideas()
    return render_template("index.html", big_ideas=big_ideas)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/login')
def login():
    return figshare.authorize(callback=url_for('authorized', _external=True))

@app.route('/post', methods=['POST'])
def post():
    client = FigshareClient(session['figshare_token'][0], session['figshare_token_secret'])
    art_id = client.post_article(request.form['title'], request.form['idea_text'])
    client.attach_idea_as_file(art_id, request.form['idea_text'])
    for cat in request.form['categories'].split(','):
        client.add_category(art_id, cat)
    client.add_tag(art_id)
    client.make_public(art_id)
    session['success'] = True
    return redirect(url_for('ideas', art_id=art_id))

@app.route('/ideas/<art_id>')
def ideas(art_id):
    success = session.pop('success', False)
    client = FigshareClient(access_token, access_token_secret)
    article = client.get_article(art_id)['items'][0]
    return render_template('idea.html', article=article, success=success)

@app.route('/search')
def search():
    q = request.values['q']
    client = FigshareClient(access_token, access_token_secret)
    results = client.search(q)
    return jsonify(results)

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
    session['figshare_token_secret'] = resp['oauth_token_secret']
    session['figshare_id'] = resp['xoauth_figshare_id']
    session['figshare_name'] = get_name_from_figshare_id(session['figshare_id'])
    return redirect(url_for('index'))

@figshare.tokengetter
def get_figshare_oauth_token():
    return session.get('figshare_token')

@app.route("/bootstrap")
def bootstrap():
    '''Bootstrap stuff for me to copy from..'''
    return render_template('bootstrap.html')

if __name__ == '__main__':
    app.run(port=80)
