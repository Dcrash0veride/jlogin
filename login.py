import hashlib
import urllib.parse
from pymongo import MongoClient
from getpass import getpass
import dbconfig

"""
TODO: Need to import argparse and do the arguments things my dudes.
"""

username = urllib.parse.quote_plus(dbconfig.db['username'])
password = urllib.parse.quote_plus(dbconfig.db['password'])
client = MongoClient("mongodb+srv://{}:{}@cluster0-sswa8.mongodb.net/test?retryWrites=true&w=majority".format(username, password))

db = client["users"]

collection = db["logins"]


def new_user():
    login = input("Username ").encode('utf-8')
    hashed_login = hashlib.sha3_512(login).hexdigest()
    if collection.count_documents({"username": hashed_login}) > 0:
        print("this username has already been taken")
        new_user()
    else:
        password = getpass('Password: ')
        encoded = password.encode('utf-8')
        hashed_password = hashlib.sha3_512(encoded).hexdigest()
        post = {"username": hashed_login, "password": hashed_password}
        collection.insert_one(post)
        print("Welcome " + login.decode())

def user_lookup():
    user_to_find = input("what is your username? ").encode('utf-8')
    hashed_to_find = hashlib.sha3_512(user_to_find).hexdigest()
    if collection.count_documents({"username": hashed_to_find}) > 0:
        results = collection.find({"username": hashed_to_find})
        for result in results:
            print(result)
    else:
        print("User NOT found")

new_user()

