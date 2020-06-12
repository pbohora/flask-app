import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class ItemObj:
    def __init__(self, name, price):
        self.name = name
        self.price = price 

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row:
            item = cls(*row)
        else:
            item = None
        
        connection.close()

        return item

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
        item = ItemObj.find_by_name(name)
        print(item)
        if item:
            return {"item":item.name,"price":item.price}          
       
        return {"message":"Item not found"}, 404


    def post(self,name):
        
        if ItemObj.find_by_name(name):
            return {"message": f"An item with name {name} already exists!"}, 400
        
        data = Item.parser.parse_args()

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        
        newItem = {"name":name,"price":data["price"]}
        query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(query, (name, data["price"]))

        connection.commit()
        connection.close()

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
