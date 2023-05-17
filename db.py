from flask import Flask
from flask_pymongo import pymongo
from app import app
CONNECTION_STRING = "mongodb+srv://m_nikhil_n:Nikhil@miniproject-2.chfsax2.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('MiniProject-2')
user_collection = pymongo.collection.Collection(db, 'Flask')


# client = pymongo.MongoClient("mongodb+srv://m_nikhil_n:<password>@miniproject-2.chfsax2.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
# db = client.test
