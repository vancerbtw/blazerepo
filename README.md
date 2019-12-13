# Blaze Repo Source
The Private Git Repo for Blaze Repo's backend rewrite implemented with python using FastAPI

# 1) Getting Setup
First you should begin by installing all of the requirements listed in the */backend/requirements.txt* file via the pip installer.
Next, you will need a certificate to allow for https connection locally (This is needed for the oauth integrations with a few services).
To do so run this command: ``openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`` in the */backend* directory
You will also need to collect a few credentials to initialize the Blaze Repo API web server.
Here is a list of the API keys you will need:
* JWT encryption secret (Basically a bunch of random characters)
* A Twitter OAuth1 Credentials ID 
* A Twitter OAuth1 Credentials Secret
* A Google OAuth2 Credentials ID 
* A Google OAuth2 Credentials Secret
* A Discord OAuth2 Client ID
* A Discord OAuth2 Client Secret
* A Zoho Email Account

Once you have set up your Twitter developer account your Twitter API App can be initialized [Here](https://developer.twitter.com/en/apps)
You can generate your Google OAuth2 credentials [Here](https://console.cloud.google.com/apis/credentials) after creating a project on the Google Cloud platform.
A Discord application may be made [Here](https://discordapp.com/developers/applications) after creating an application you may retrieve your credentials.
To receive a Blaze Repo email please contact me privately.
All services will require a callback url to be set. All callback URLs will be set to: ``https://localhost:5000/auth/callback/<service_name>``
Example: ``https://localhost:5000/auth/callback/discord``

A PostgreSQL databse will need to initialized and setup before initializing your Blaze Repo API web server instance. You can run your database locally or in the cloud.
* [Setting up a database locally on Windows](https://www.microfocus.com/documentation/idol/IDOL_12_0/MediaServer/Guides/html/English/Content/Getting_Started/Configure/_TRN_Set_up_PostgreSQL.htm)
* [Setting up a database locally on Mac OSX](https://www.tunnelsup.com/setting-up-postgres-on-mac-osx/)
* [Setting up a database locally on Linux](http://www.yolinux.com/TUTORIALS/LinuxTutorialPostgreSQL.html)
*Cloud initialization of a PostgreSQL instance will vary based on your hosting provider of choice*

No tables will be required to be created, as this python app will dynamically generate said tables and schemas upon running.
Only a database instance will be required to be created if not done already.

You will need to supply a database connection URI.
This URI will be formatted as follows:
*postgresql://**user**:**password**@**host**:**port**/**database**

All of these credentials will be inputted in a .env file that will be placed in the */backend* directory.

A sample *.env* file has been supplied in the root of this repository.

# 2) Running
To run Blaze Repo API web server instance navigate to the *./backend* directory and execute the following command:
``FLASK_APP=main.py FLASK_ENV=development flask run --cert=cert.pem --key=key.pem``
This will initialize the web server and allow for SSL connections.
This environment is strictly for development purposes and it is not recommended to use this runtime environment in production level deployments.

# 3) Accessing the API
You can connect to the API at https://localhost:5000/
**HTTPS PROTOCOL MUST BE USED**
