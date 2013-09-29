import json
from cStringIO import StringIO

import requests
from requests_oauthlib import OAuth1

from figshare_credentials import (
    consumer_key,
    consumer_secret,
)

HEADERS = {'content-type':'application/json'}

def get_name_from_figshare_id(figshare_id):
    res = requests.get("http://figshare.com/authors/Unknown/%s" % figshare_id)
    #XXX replace with lxml or beautifulsoup
    #XXX or ask them to make an API call for this (unless i missed it)
    name = res.content.split('id="author_name">')[1].split("<", 1)[0]
    return name

#XXX: i was getting an "incorrect base string" API response when using flask-oauthlib
#XXX: could only get the API calls to work by manually creating the OAuth1 client
#XXX: need to go back through the flask-oauthlib examples and make sure i'm sending oauth_token_secret

class FigshareClient(object):
    def __init__(self, key, secret):
        self.oauth = OAuth1(
            client_key=consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=key,
            resource_owner_secret=secret,
            signature_type='auth_header'
        )
        self.client = requests.session()

    def post_article(self, title, description):
        body = {'title':title, 'description': description, 'defined_type': 'paper'}
        res = self.client.post('http://api.figshare.com/v1/my_data/articles', auth=self.oauth, data=json.dumps(body), headers=HEADERS)
        res = json.loads(res.content)
        return res['article_id']

    def attach_idea_as_file(self, art_id, idea_text):
        files = {'filedata': ('idea.txt', StringIO(idea_text))}
        res = self.client.put('http://api.figshare.com/v1/my_data/articles/%s/files' % art_id, auth=self.oauth, files=files)
        res = json.loads(res.content)
        return res

    def add_category(self, art_id, cat_id):
        body = {'category_id': cat_id}
        res = self.client.put('http://api.figshare.com/v1/my_data/articles/%s/categories' % art_id, auth=self.oauth, data=json.dumps(body), headers=HEADERS)
        res = json.loads(res.content)
        return res

    def add_tag(self, art_id, tag_name="Journal of Brief Ideas"):
        body = {'tag_name': tag_name}
        res = self.client.put('http://api.figshare.com/v1/my_data/articles/%s/tags' % art_id, auth=self.oauth, data=json.dumps(body), headers=HEADERS)
        res = json.loads(res.content)
        return res

    def make_public(self, art_id):
        res = self.client.post('http://api.figshare.com/v1/my_data/articles/%s/action/make_public' % art_id, auth=self.oauth, headers=HEADERS)
        res = json.loads(res.content)
        return res

    def get_article(self, art_id):
        res = self.client.get('http://api.figshare.com/v1/articles/%s' % art_id, auth=self.oauth)
        res = json.loads(res.content)
        return res
