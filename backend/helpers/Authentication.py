import jwt
from jwt import PyJWTError
from database.Database import Database
from models.User import User
from passlib.context import CryptContext
from starlette.requests import Request


class Authentication:
    def __init__(self, secret):
        self.secret = secret
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)

    def register_check(self, name, email, password, password_confirm, db):
        if name == "" or email == "" or password == "" or password_confirm == "":
            return "All fields must have an inputted value."
        if not db.user_exists(email):
            if password == password_confirm:
                return User(name, email, False, self.get_password_hash(password))
            else:
                return "Passwords do not match."
        else:
            return "User with same email is already registered."

    def login(self, email, password, db):
        if user := db.get_user(email):
            if self.verify_password(password, user.password):
                return user
            return "Password is incorrect."
        return "Invalid email address."

