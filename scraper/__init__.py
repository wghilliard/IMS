from mongoengine import connect
from pymongo import read_preferences
import config
from celery import Celery

# Celery
worker = Celery('ims')
worker.config_from_object(config)

# MongoDB
read_preference = read_preferences.ReadPreference.PRIMARY
db = connect(db=config.MONGODB_DB, host=config.MONGODB_HOST, port=config.MONGODB_PORT, read_preference=read_preference)

