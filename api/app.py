from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from auth import authenticate, identity
from user import UserRegister
from item import Item, ItemList

import config

app = Flask(__name__)
app.secret_key = config.secret
api = Api(app)

jwt = JWT(app, authenticate, identity)          #JWT creates a new end point /auth 


api.add_resource(ItemList, "/items")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(UserRegister, "/signup")

if __name__ == "__main__":
    app.run(port=3000, debug = True)