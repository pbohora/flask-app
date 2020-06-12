from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity

from auth import authenticate, identity

import config

app = Flask(__name__)
app.secret_key = config.secret
api = Api(app)

jwt = JWT(app, authenticate, identity)          #JWT creates a new end point /auth 

items=[]

class ItemList(Resource):
    def get(self):
        return {"items": items}, 200


class Item(Resource):                             #create resource Item
    parser=reqparse.RequestParser()  
    parser.add_argument("price",                  #only get the arguments that are ther part of the RequestParser
        type = float,
        required = True,
        help = "This is a required filed!!"
    )


    def get(self, name):
        item = next(filter(lambda x : x["name"] == name, items), None)
        return {"item": item}, 200 if item else 400

    def post(self,name):
        if next(filter(lambda x : x["name"] == name, items), None) is not None:
            return {"message": f"An item with name {name} already exists!"}, 400
        
        data = Item.parser.parse_args()

        newItem = {"name": name, "price": data["price"] }

        items.append(newItem)

        return newItem, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message":f"Item {name} deleted"}, 204

    @jwt_required()
    def put(self, name): 
        data = Item.parser.parser()

        item = next(filter(lambda x : x["name"] == name, items), None)

        if items is None: 
            newItem = {"name":name, "price": data["price"]}
            items.append(newItem)
        else:
            item.update(data)

        return item

api.add_resource(ItemList, "/items")
api.add_resource(Item, "/item/<string:name>")

if __name__ == "__main__":
    app.run(port=3000, debug = True)