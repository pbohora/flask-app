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

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        
        query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(query, (item["name"], item["price"]))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        
        query = "UPDATE items SET price=? where name=?"
        cursor.execute(query, (item["price"], item["name"]))

        connection.commit()
        connection.close()

    @classmethod
    def remove(cls,name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        
        query = "DELETE FROM items where name = ?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()


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
        try:
            item = ItemObj.find_by_name(name)
        except:
            return {"message":"Error occur while getting an item"}, 500
        
        if item:
            return {"item":item.name,"price":item.price}          
       
        return {"message":"Item not found"}, 404


    def post(self,name):
        
        if ItemObj.find_by_name(name):
            return {"message": f"An item with name {name} already exists!"}, 400
        
        data = Item.parser.parse_args()

        new_item = {"name":name,"price":data["price"]}

        try:
            ItemObj.insert(new_item)
        except:
            return{"message":"Error occur while inserting an item"}, 500

        return newItem, 201

    @jwt_required()
    def delete(self, name):
        try:
            ItemObj.remove(name)
        except:
            return{"message":"Error occur while removing an item"}, 500
        
        return {"message":f"Item {name} deleted"}, 204

    @jwt_required()
    def put(self, name): 
        data = Item.parser.parse_args()

        item = ItemObj.find_by_name(name)
        updated_item = {"name":name, "price":data["price"]}

        if item is None: 
            try:
                ItemObj.insert(updated_item)
            except:
                return{"message":"Error occur while inserting an item"}, 500            
        else:
            try:
                ItemObj.update(updated_item)
            except:
                return{"message":"Error occur while updating an item"}, 500

        return updated_item
