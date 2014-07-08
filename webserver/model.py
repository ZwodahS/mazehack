import pymongo
from mazehack.mazedef import to_maze
from webserver import app
from flask import g, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import mazehack.generator as generator
import random
import string
######################### DB CODE ########################
def connect_db(url) :
    client = MongoClient(url);
    return client

def get_db():
    if not hasattr(g, "mongo"):
        g.mongo = connect_db(app.config["DATABASE_URL"])
        g.database = g.mongo[app.config["DATABASE_NAME"]]
    return g.database

# @app.teardown_appcontext
def close_db(error):
    if hasattr(g, "mongo"):
        g.mongo.close();

def random_string(size):
    return "".join([random.choice(string.ascii_letters + string.digits) for i in range(0, size)])



def db_add_maze(maze, random_id = None):
    if random_id is None :
        random_id = random_string(30)
    db = get_db()
    while True:
        found = db["mazes_id"].find({ "value" : random_id})
        if found.count() == 0:
            break
        print("Duplicate Id : ", random_id)
        print("Generating a new one")
        random_id = random_string(30)
    maze["maze_id"] = random_id

    db["mazes"].insert(maze)
    db["mazes_id"].insert({ "value" : random_id})

    print("Maze added and given the id", random_id)

def db_get_maze(id):
    db = get_db()
    found = db["mazes"].find( {"maze_id" : id} )
    if found.count() == 0 :
        return None
    else :
        return to_maze(found[0])

def db_reset_mazes():
    db = get_db()
    # generate entrance
    db["mazes"].remove({})
    db["mazes_id"].remove({})

    maze = generator.generate_maze(51, 51, {})
    db_add_maze(maze, "entrance")
