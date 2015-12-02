from mongoengine import connect
from pymongo import read_preferences
import config
from celery import Celery

# Celery
worker = Celery('ims')
worker.config_from_object(config)

# Mongo
read_preference = read_preferences.ReadPreference.PRIMARY
db = connect(db=config.MONGODB_DB, host=config.MONGODB_HOST, port=config.MONGODB_PORT, read_preference=read_preference)


# NEXT THING TODO WAS ADDING START TO CELERY TASKS

# start('COMS', '1301', uuid4())
