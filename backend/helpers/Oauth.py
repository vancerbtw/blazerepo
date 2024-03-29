from flask import request, session, redirect, url_for
from rauth import OAuth2Service, OAuth1Service
from models.User import User
from models.Twitter import Twitter
import google.oauth2.credentials
import google_auth_oauthlib.flow
from models.Google import Google
from models.Discord import Discord
from flask_discord import DiscordOAuth2Session, configs
from flask_mail import Message
from helpers.Authentication import verify_email_send, make_session_user


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
        request_token = self.service.get_request_token(
            params={'oauth_callback': "http://localhost:5000/auth/callback/twitter"})
        session['request_token'] = request_token
        return redirect(self.service.get_authorize_url(request_token[0]))

    def callback(self, db, mail):
        request_token = session.pop('request_token')
        if 'oauth_verifier' not in request.args:
            return
        twitter_response = self.service.get_auth_session(request_token[0], request_token[1],
                                                         data={'oauth_verifier': request.args['oauth_verifier']}).get(
            'account/verify_credentials.json', params={'include_email': 'true'}).json()
        if db.check_twitter(twitter_response['id_str']):
            user_id = None
            if db.user_exists(twitter_response['email']) is False:
                user = User(twitter_response['screen_name'], twitter_response['email'], False)
                user_id = db.add_user(user)
                verify_email_send(twitter_response['email'], user.emailToken, mail)
            else:
                return "A Blaze account is already using the email associated with this twitter, please link this account in the account settings."
            print(user_id)
            db.add_twitter(
                Twitter(twitter_response['id_str'], twitter_response['email'], twitter_response['screen_name'],
                        user_id))
            return make_session_user(db.get_user_by_id(user_id))
        else:
            if user_id := db.twitter_user_id(twitter_response['id_str']):
                return make_session_user(db.get_user_by_id(user_id))
            return "Internal server error"


class GoogleSignIn(OAuthSignIn):
    def __init__(self, creds):
        super(GoogleSignIn, self).__init__('google', creds)
        self.service = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=[
            "https://www.googleapis.com/auth/userinfo.email", "openid",
            "https://www.googleapis.com/auth/userinfo.profile"])
        self.service.redirect_uri = 'https://127.0.0.1:5000/auth/callback/google'  # url_for('auth_google_callback', _external=True)

    def authorize(self):
        authorization_url, session['state'] = self.service.authorization_url(access_type='offline',
                                                                             include_granted_scopes='true')
        return redirect(authorization_url)

    def callback(self, db, mail):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=[
            "https://www.googleapis.com/auth/userinfo.email", "openid",
            "https://www.googleapis.com/auth/userinfo.profile"], state=session['state'])
        flow.redirect_uri = 'https://127.0.0.1:5000/auth/callback/google'
        flow.fetch_token(authorization_response=request.url)
        google_user = flow.authorized_session().get('https://www.googleapis.com/userinfo/v2/me').json()
        print(google_user)
        if db.check_google(google_user['id']):
            user_id = None
            if db.user_exists(google_user['email']) is False:
                user = User(google_user['name'], google_user['email'], False)
                user_id = db.add_user(user)
                verify_email_send(google_user['email'], user.emailToken, mail)

            else:
                return "A Blaze account is already using the email associated with this Google account, please link this account on the account settings page."
            print(user_id)
            db.add_google(Google(google_user, user_id))
            return make_session_user(db.get_user_by_id(user_id))
        else:
            if user_id := db.google_user_id(google_user['id']):
                return make_session_user(db.get_user_by_id(user_id))
            return "Internal server error"


class DiscordSignIn():
    def __init__(self, app):
        self.auth = DiscordOAuth2Session(app)

    def authorize(self):
        return self.auth.create_session(['identify', 'email'])

    def build_session(self):
        if request.values.get("error"):
            return request.values["error"]
        session["DISCORD_OAUTH2_TOKEN"] = self.auth._make_session(
            state=session.get("DISCORD_OAUTH2_STATE")).fetch_token(configs.TOKEN_URL,
                                                                   client_secret=self.auth.client_secret,
                                                                   authorization_response=request.url)

    def callback(self, db, mail):
        if error := self.build_session():
            return error
        discord_user = self.auth.fetch_user()
        discord_user.id = str(discord_user.id)
        if db.check_discord(discord_user.id):
            user_id = None
            if db.user_exists(discord_user.email) is False:
                user = User(discord_user.username, discord_user.email, False)
                user_id = db.add_user(user)
                verify_email_send(discord_user.email, user.emailToken, mail)
            else:
                return "A Blaze account is already using the email associated with this Google account, please link this account on the account settings page."
            db.add_discord(Discord(discord_user, user_id))
            return make_session_user(db.get_user_by_id(user_id))
        else:
            if user_id := db.discord_user_id(discord_user.id):
                user = db.get_user_by_id(user_id)
                return make_session_user(db.get_user_by_id(user_id))
            return "Internal server error"
