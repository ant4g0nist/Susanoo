from mongoengine import *

MONGO_DBNAME = "susanoo"
MONGO_URI    = "mongodb://localhost:27017/"+MONGO_DBNAME

db = connect(host=MONGO_URI)
