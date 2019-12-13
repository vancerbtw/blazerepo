from imports import *
load_dotenv()  # importing credentials

app = Flask(__name__,
            static_url_path='/static',
            static_folder='../frontend/public',
            template_folder='../frontend/templates')

app.secret_key = os.getenv("JWT_SECRET")

auth = Authentication(os.getenv("JWT_SECRET"))
oauth = OAuth(app)
db = Database(os.getenv("DB_URI"))

app.config['OAUTH_CREDENTIALS'] = {
    'twitter': {
        'id': os.getenv('TWITTER_ID'),
        'secret': os.getenv('TWITTER_SECRET')
    },
    'google': {
        'id': os.getenv('GOOGLE_ID'),
        'secret': os.getenv('GOOGLE_SECRET')
    }
}

app.config["DISCORD_CLIENT_ID"] = os.getenv("DISCORD_ID")  # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_SECRET")  # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "https://localhost:5000/auth/callback/discord"  # Redirect URI.
app.config['MAIL_SERVER'] = os.getenv('EMAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('EMAIL_PORT')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')

mail = Mail(app)

user_hash = Hashids(salt=os.getenv('USER_ID_HASH'), min_length=6)

@app.route("/")
def root():
    user = None
    if 'user' in session:
        user = session['user']
    return render_template("index.html", user=user)


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
            session['user'] = make_session_user(user)
            return redirect(redirect_url, code=302)
        return {
            "error": user
        }
    raise {
        "error": "Internal Server Error."
    }


@app.route("/register", methods=['POST'])
def register_local():
    if user := auth.register_check(request.form.get('name'), request.form.get('email'), request.form.get('password'), request.form.get('password2'), db):
        if isinstance(user, User):
            auth.register_user(user, db, mail)
            return redirect("/login?success=User Successfully Registered", code=302)
        return user
    return "Internal server error"


@app.route("/auth/twitter")
def auth_twitter():
    session['redirect'] = request.args.get('redirect', default="https://blazerepo.com/", type=str)
    return TwitterSignIn(app.config['OAUTH_CREDENTIALS']['twitter']).authorize()


@app.route("/auth/callback/twitter")
def auth_twitter_callback():
    user = TwitterSignIn(app.config['OAUTH_CREDENTIALS']['twitter']).callback(db, mail)
    if isinstance(user, str):
        return redirect(f"/login?redirect={session['redirect']}&error={user}", code=302)
    session['user'] = user
    print(user)
    return redirect(session['redirect'], code=302)


@app.route("/auth/google")
def auth_google():
    session['redirect'] = request.args.get('redirect', default="https://blazerepo.com/", type=str)
    return GoogleSignIn(app.config['OAUTH_CREDENTIALS']['google']).authorize()


@app.route("/auth/callback/google")
def auth_google_callback():
    user = GoogleSignIn(app.config['OAUTH_CREDENTIALS']['google']).callback(db, mail)
    if isinstance(user, str):
        return redirect(f"/login?redirect={session['redirect']}&error={user}", code=302)
    session['user'] = user
    return redirect(session['redirect'], code=302)

@app.route("/auth/discord")
def auth_discord():
    session['redirect'] = request.args.get('redirect', default="https://blazerepo.com/", type=str)
    return DiscordSignIn(app).authorize()


@app.route("/auth/callback/discord")
def auth_discord_callback():
    user = DiscordSignIn(app).callback(db, mail)
    if isinstance(user, str):
        return redirect(f"/login?redirect={session['redirect']}&error={user}", code=302)
    session['user'] = user
    print(user)
    return redirect(session['redirect'], code=302)


@app.route("/user/verify/<verify_token>")
def verify_user(verify_token):
    if user := session['user']:
        if user['verified']:
            return render_template("error.html", error="User is already verified", code=409)
        if verification := db.verify_user(user, verify_token):
            if verification:
                user['verified'] = True
                session['user'] = user
                return "Verification Complete"
            return render_template("error.html", error=verification, code=409)
    return redirect(f'/login?redirect=/user/verify/{verify_token}')


@app.route("/account")
def present_account():
    if 'user' in session:
        return render_template("account.html", linked_accounts=db.get_linked_accounts(session['user']), balance=db.get_user_balance(session['user']['id']), user_id=user_hash.encode(session['user']['id']).upper(), user=session['user'], purchases=db.get_user_purchases(session['user']['id']))
    return redirect("/login?redirect=/account")


@app.route("/add/package/<package>/<price>")
def add_package(package, price):
    db.insert_package(package, float(price))
    return {
        "inserted!": "done"
    }


@app.route("/add/downloads/<package>")
def add_downloads(package):
    for i in range(1000):
        db.add_download(package)
    return {
        "done": True
    }


@app.route("/check/downloads/<package>/<days>")
def check_downloads(package, days):
    if total := get_total_downloads(db, package, int(days)):
        return {
            "total": total
        }


@app.route("/purchase/<packageid>")
def purchase_page(packageid):
    if user := session['user']:
        print(user)
        if db.is_package(packageid):
            if package := db.info_package(packageid):
                return render_template("purchase.html", gift=False, packageid=packageid, giftUser="", token="",
                                       userId="", user=user)
            return {
                "Irror": "Could not locate package info."
            }
        return {
            "Error": f"Package: {packageid} does not exist"
        }
    return redirect(f"/login?redirect=/purchase/{packageid}", code=302)


@app.route("/dev/users/me")
def show_me():
    user = session['user']
    return {
        "id": user['id'],
        "username": user['username'],
        "disabled": user['disabled'],
        "verified": user['verified'],
        "profile_pic": user['profile_pic'],
        "admin": user['admin'],
        "developer": user['developer']
    }


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.config['SERVER_NAME'] = 'vibhu.gfg:5000'
    app.run(ssl_context=('cert.pem', 'key.pem'))
