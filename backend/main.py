from flask import Flask, render_template, request, session, redirect
from dotenv import load_dotenv
import os

# importing auth and modules
from helpers.Authentication import Authentication
from models.User import User

# importing database class
from database.Database import Database

load_dotenv()  # importing credentials

app = Flask(__name__,
            static_url_path='/static',
            static_folder='../frontend/public',
            template_folder='../frontend/templates')

app.secret_key = os.getenv("JWT_SECRET")

auth = Authentication(os.getenv("JWT_SECRET"))

db = Database(os.getenv("DB_URI"))

@app.route("/")
def root():
    user = None
    username = ""
    if session.get('user', None):
        if user := session['user']:
            username = user.get("username", "")

    return render_template("index.html", user=user, )


@app.route("/login")
def present_login():
    if session.get('user', None) is None:
        return render_template("login.html", redirect=request.args.get('redirect', default="https://blazerepo.com/", type=str))
    return redirect(request.args.get('redirect', default="https://blazerepo.com/", type=str), code=302)

@app.route("/logout")
def logout():
    if session.get('user', None):
        session['user'] = None
    return redirect("https://blazerepo.com/", 302)


@app.route("/auth/login", methods=['POST'])
def authenticate_local():
    redirect_url = request.args.get('redirect', default="https://blazerepo.com/", type=str)
    email = request.form.get('email')
    password = request.form.get('password')
    if user := auth.login(email, password, db):
        if type(user) != str:
            session['user'] = {
                "username": user.username,
                "email": user.email,
                "disabled": user.disabled,
                "verified": user.verified
            }
            return redirect(redirect_url, code=302)
        return {
            "error": user
        }
    raise {
        "error": "Internal Server Error."
    }
#
#
@app.route("/register", methods=['POST'])
def register_local():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if user := auth.register_check(name, email, password, password2, db):
        if isinstance(user, User):
            db.add_user(user)
            return redirect("/login?showSignUp=true&success=User Successfully Registered", code=302)
        return user
    return user


@app.route("/account")
def present_account():
    print(session['test1'])
    return {
        "test": "Test!"
    }

if __name__ == '__main__':
    app.run()
