from flask import Flask, render_template, request, session, redirect
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

# importing auth and modules
from helpers.Authentication import Authentication, verify_email_send, make_session_user
from helpers.Oauth import OAuthSignIn, TwitterSignIn, GoogleSignIn, DiscordSignIn
from models.User import User
from models.Package import get_total_downloads

# importing database class
from database.Database import Database
from flask_mail import Mail, Message