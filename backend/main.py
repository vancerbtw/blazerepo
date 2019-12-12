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


@app.route("/")
def root():
    user = None
    username = ""
    if session.get('user', None):
        if user := session['user']:
            username = user.get("username", "")

    return render_template("index.html", user=user, username=username)


@app.route("/login")
def present_login():
    if session.get('user', None) is None:
        return render_template("login.html",
                               redirect=request.args.get('redirect', default="https://blazerepo.com/", type=str))
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
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "disabled": user.disabled,
                "verified": user.verified,
                "admin": user.admin
            }
            return redirect(redirect_url, code=302)
        return {
            "error": user
        }
    raise {
        "error": "Internal Server Error."
    }


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


@app.route("/auth/twitter")
def auth_twitter():
    session['redirect'] = request.args.get('redirect', default="https://blazerepo.com/", type=str)
    return TwitterSignIn(app.config['OAUTH_CREDENTIALS']['twitter']).authorize()


@app.route("/auth/callback/twitter")
def auth_twitter_callback():
    user = TwitterSignIn(app.config['OAUTH_CREDENTIALS']['twitter']).callback(db)
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
    user = GoogleSignIn(app.config['OAUTH_CREDENTIALS']['google']).callback(db)
    if isinstance(user, str):
        return redirect(f"/login?redirect={session['redirect']}&error={user}", code=302)
    session['user'] = user
    return redirect(session['redirect'], code=302)

@app.route("/users/me")
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


@app.route("/account")
def present_account():
    return {
        "test": "Test!"
    }


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


if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))
