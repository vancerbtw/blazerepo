from flask import Flask, render_template, request, session, redirect
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

# importing auth and modules
from helpers.Authentication import Authentication
from models.User import User
from models.Package import get_total_downloads

# importing database class
from database.Database import Database