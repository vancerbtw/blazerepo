from flask import request, session, redirect, url_for
from rauth import OAuth2Service, OAuth1Service
from models.User import User, verify_email_send
from models.Twitter import Twitter
import google.oauth2.credentials
import google_auth_oauthlib.flow
from models.Google import Google

class OAuthSignIn():
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

    def callback(self, db):
        request_token = session.pop('request_token')
        if 'oauth_verifier' not in request.args:
            return
        twitter_response = self.service.get_auth_session(request_token[0], request_token[1], data={'oauth_verifier': request.args['oauth_verifier']}).get('account/verify_credentials.json', params={'include_email':'true'}).json()
        if db.check_twitter(twitter_response['id_str']):
            user_id = None
            if db.user_exists(twitter_response['email']) is False:
                user_id = db.add_user(User(twitter_response['screen_name'], twitter_response['email'], False))
                verify_email_send(twitter_response['email'])
            else:
                return "A Blaze account is already using the email associated with this twitter, please link this account in the account settings."
            print(user_id)
            db.add_twitter(Twitter(twitter_response['id_str'], twitter_response['email'], twitter_response['screen_name'], user_id))
            user = db.get_user_by_id(user_id)
            return {
                "id": user.id,
                "username": user.username,
                "disabled": user.disabled,
                "verified": user.verified,
                "profile_pic": user.profile_pic,
                "admin": user.admin,
                "developer": user.developer
            }
        else:
            if user_id := db.twitter_user_id(twitter_response['id_str']):
                user = db.get_user_by_id(user_id)
                return {
                    "id": user.id,
                    "username": user.username,
                    "disabled": user.disabled,
                    "verified": user.verified,
                    "profile_pic": user.profile_pic,
                    "admin": user.admin,
                    "developer": user.developer
                }
            return "Internal server error"

class GoogleSignIn(OAuthSignIn):
    def __init__(self, creds):
        super(GoogleSignIn, self).__init__('google', creds)
        self.service = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=["https://www.googleapis.com/auth/userinfo.email", "openid", "https://www.googleapis.com/auth/userinfo.profile"])
        self.service.redirect_uri = 'https://127.0.0.1:5000/auth/callback/google' #url_for('auth_google_callback', _external=True)

    def authorize(self):
        authorization_url, session['state'] = self.service.authorization_url(access_type='offline',include_granted_scopes='true')
        return redirect(authorization_url)

    def callback(self, db):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=["https://www.googleapis.com/auth/userinfo.email", "openid", "https://www.googleapis.com/auth/userinfo.profile"], state=session['state'])
        flow.redirect_uri = 'https://127.0.0.1:5000/auth/callback/google'
        flow.fetch_token(authorization_response=request.url)
        google_user = flow.authorized_session().get('https://www.googleapis.com/userinfo/v2/me').json()
        print(google_user)
        if db.check_google(google_user['id']):
            user_id = None
            if db.user_exists(google_user['email']) is False:
                user_id = db.add_user(User(google_user['name'], google_user['email'], False))
                verify_email_send(google_user['email'])
            else:
                return "A Blaze account is already using the email associated with this Google account, please link this account on the account settings page."
            print(user_id)
            db.add_google(Google(google_user, user_id))
            user = db.get_user_by_id(user_id)
            return {
                "id": user.id,
                "username": user.username,
                "disabled": user.disabled,
                "verified": user.verified,
                "profile_pic": user.profile_pic,
                "admin": user.admin,
                "developer": user.developer
            }
        else:
            if user_id := db.google_user_id(google_user['id']):
                user = db.get_user_by_id(user_id)
                return {
                    "id": user.id,
                    "username": user.username,
                    "disabled": user.disabled,
                    "verified": user.verified,
                    "profile_pic": user.profile_pic,
                    "admin": user.admin,
                    "developer": user.developer
                }
            return "Internal server error"