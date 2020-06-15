from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from auth import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

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


api.add_resource(ItemList, "/items")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(UserRegister, "/signup")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=3000, debug = True)