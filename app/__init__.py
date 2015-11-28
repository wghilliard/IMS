from flask import Flask
from mongoengine import connect
from pymongo import read_preferences
import config
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt

# Flask
app = Flask(__name__)
app.config.from_object('config')


# Mongo
read_preference = read_preferences.ReadPreference.PRIMARY
db = connect(db=config.MONGODB_DB, host=config.MONGODB_HOST, port=config.MONGODB_PORT, read_preference=read_preference)

# Flask-Login
lm = LoginManager()
lm.init_app(app)

# Flask-Bcrypt
bcrypt = Bcrypt(app)

# Import was placed here to stop circular imports.
from app import views, models, api
