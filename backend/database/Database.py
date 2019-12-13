from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy.orm import sessionmaker
from database.Base import Base
from models.User import User
from models.Purchase import Purchase
from models.Twitter import Twitter
from models.Package import Package
from models.Google import Google
from models.Discord import Discord
from models.Deposit import Deposit
from models.Wallet import Wallet
import datetime


class Database:
    def __init__(self, connection_string):
        self.db = create_engine(connection_string)
        Session = sessionmaker(bind=self.db)
        self.session = Session()
        Base.metadata.create_all(self.db)
        self.session.commit()

    def add_user(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        self.session.add(Wallet(user.id))
        return user.id

    def user_exists(self, email: str = None):
        exists = self.session.query(
            self.session.query(User).filter_by(email=email).exists()
        ).scalar()
        return exists

    def get_user(self, email: str = None):
        return self.session.query(User).filter(User.email == email).first()

    def get_user_by_id(self, id: int = None):
        return self.session.query(User).filter(User.id == id).first()

    def insert_package(self, package: str = None, price: float = 0.00):
        self.session.add(Package(package, "supremevance123", price))
        self.session.commit()

    def add_download(self, package: str = None):
        if downloads := self.session.query(Package).filter(Package.packageid == package).first():
            downloads.downloads.append(datetime.date.today())
            self.session.commit()
            return

    def get_downloads(self, package):
        if downloads := self.session.query(Package).filter(Package.packageid == package).first():
            return downloads.downloads

    def add_purchase(self, user, processor, package, price, discount):
        if self.session.query(Purchase).filter(Purchase.purchaser_id == user.id and Purchase.package == package).count() <= 0:
            self.session.add(Purchase(user["id"], processor, package, price, discount))
            return True
        return False

    def is_package(self, package):
        if package := self.session.query(Package).filter(Package.packageid == package).first():
            return package
        return

    def info_package(self, package):
        if package := self.session.query(Package).filter(Package.packageid == package).first():
            return package
        return

    def add_twitter(self, twitter):
        self.session.add(twitter)
        self.session.commit()

    def check_twitter(self, id):
        if self.session.query(Twitter).filter(Twitter.twitter_id == id).count() <= 0:
            return True
        return False

    def twitter_user_id(self, id):
        if twitter := self.session.query(Twitter).filter(Twitter.twitter_id == id).first():
            return twitter.user_id
        return

    def add_google(self, google):
        self.session.add(google)
        self.session.commit()

    def check_google(self, id):
        if self.session.query(Google).filter(Google.google_id == id).count() <= 0:
            return True
        return False

    def google_user_id(self, id):
        if google := self.session.query(Google).filter(Google.google_id == id).first():
            return google.user_id
        return


    def add_discord(self, discord):
        self.session.add(discord)
        self.session.commit()

    def check_discord(self, id):
        if self.session.query(Discord).filter(Discord.discord_id == id).count() <= 0:
            return True
        return False

    def discord_user_id(self, id):
        if discord := self.session.query(Discord).filter(Discord.discord_id == id).first():
            return discord.user_id
        return

    def verify_user(self, session_user, token):
        print(session_user)
        if user := self.session.query(User).filter(User.email == session_user['email']).first():
                if user.emailToken == token:
                    user.verified == True
                    self.session.commit()
                    return True
                return "Invalid Verification URL"
        return "Internal Server Error"

    def get_linked_accounts(self, user):
        accounts = {'linked': []}
        if discord_result := self.session.query(User, User.discord.has()).filter(User.email == user['email']).first():
            if discord_result[1]:
                accounts['linked'].append({'type': "discord", 'account': discord_result[0].discord.name})
        print(self.session.query(User, User.twitter.has()).filter(User.email == user['email']))
        if twitter_result := self.session.query(User, User.twitter.has()).filter(User.email == user['email']).first():
            if twitter_result[1]:
                accounts['linked'].append({'type': "twitter", 'account': twitter_result[0].twitter.name})

        if google_result := self.session.query(User, User.google.has()).filter(User.email == user['email']).first():
            if google_result[1]:
                accounts['linked'].append({'type': "google", 'account': google_result[0].google.name})

        return accounts

    def get_user_purchases(self, user_id):
        return self.session.query(Purchase).filter(Purchase.user_id == user_id).all()

    def get_user_balance(self, user_id):
        return self.session.query(User).filter(User.id == int(user_id)).first().wallet.amount

