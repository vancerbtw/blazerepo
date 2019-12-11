from flask import session, redirect, url_for, request
from rauth import OAuth2Service, OAuth1Service

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name, creds):
        self.provider_name = provider_name
        self.consumer_id = creds['id']
        self.consumer_secret = creds['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class TwitterSignIn(OAuthSignIn):
    def __init__(self, creds):
        super(TwitterSignIn, self).__init__('twitter', creds)
        self.service = OAuth1Service(
            name='twitter',
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            request_token_url='https://api.twitter.com/oauth/request_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            access_token_url='https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1.1/'
        )

    def authorize(self):
        request_token = self.service.get_request_token(params={'oauth_callback': "http://localhost:5000/auth/callback/twitter"})
        session['request_token'] = request_token
        return redirect(self.service.get_authorize_url(request_token[0]))

    def callback(self):
        request_token = session.pop('request_token')
        if 'oauth_verifier' not in request.args:
            return
        twitter_response = self.service.get_auth_session(request_token[0], request_token[1], data={'oauth_verifier': request.args['oauth_verifier']}).get('account/verify_credentials.json', params={'include_email':'true'}).json()
        return twitter_response['id_str'], twitter_response['screen_name'], twitter_response['email']