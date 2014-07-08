import os 
import sys
import pymongo
from bson.objectid import ObjectId
from flask import Flask
from pymongo import MongoClient
##########################################################

MONGO_URL = os.environ.get('MONGOHQ_URL')
MONGO_DB = os.environ.get('MONGOHQ_DBNAME')
if MONGO_URL == None:
    MONGO_URL = "mongodb://localhost:27017"  # for development environmnet, set it to local host
    print("Development environment, mongodb location at " + MONGO_URL)
if MONGO_DB == None:
    MONGO_DB = "main"
print("Mongo URL : " + MONGO_URL)
print("Using DB : " + MONGO_DB)

app = Flask(__name__);
# change this from the dict() initializer to {} instead. Looks nicer.
# I don't like key value of a dict to be "non-string", looks like variable to me.
app.config.update({
    "DATABASE_URL" : MONGO_URL,
    "DATABASE_NAME" : MONGO_DB,
    "DEBUG" : True,
    "SECRET_KEY" : "A9jexoyoV4C2r0MxnqQJq3soEE6qPYCS2fED2PlUEupr7krh4S+vwTV1MopWVQ/8Yh2I4gCPEXK//prc6Qgr1pwPpEeabsT7bx0guo1gkXlD6PX4yVYfIR1CylICbtDOSrPgZ0gZI3DHEiztMu1S9OuloDi7hdhFLbkeNnhayBQ=",
    "GENERATEMAZE_KEY" : "WXKSCP121uAFMkO6sGuZQ"
    })


import webserver.views
