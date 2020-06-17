import json
from flask import Flask,request,redirect,url_for
from flask_restful import Api
from flask_jwt import JWT
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
from models.user import UserModel
import requests

from auth import authenticate, identity
from resources.user import UserRegister, UserLogin, UserLog
from resources.item import Item, ItemList
from resources.category import Category, CategoryList

import configurations

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = configurations.secret
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)          #JWT creates a new end point /auth 

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    print(user)
    return User.get(user_id)

api.add_resource(CategoryList, "/categories")
api.add_resource(ItemList, "/items")
api.add_resource(Category, "/category/<string:name>")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(UserRegister, "/signup")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLog, "/login/callback")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(ssl_context=('cert.pem', 'key.pem'), port=3000, debug = True)