import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        
        query = "SELECT * FROM items"
        result= cursor.execute(query)
        items=[]

        for row in result:
            items.append({"name":row[0], "price":row[1]})
    
        connection.close()
        print(items)

        return {"items":items}


class Item(Resource):                             #create resource Item

    parser=reqparse.RequestParser()  
    parser.add_argument("price",                  #only get the arguments that are ther part of the RequestParser
        type = float,
        required = True,
        help = "This is a required filed!!"
    )

    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message":"Error occur while getting an item"}, 500
        
        if item:
            return item.json()          
       
        return {"message":"Item not found"}, 404


    def post(self,name):
        
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name {name} already exists!"}, 400
        
        data = Item.parser.parse_args()

        new_item = ItemModel(name, data["price"])

        try:
            new_item.insert()
        except:
            return{"message":"Error occur while inserting an item"}, 500

        return new_item.json(), 201

    @jwt_required()
    def delete(self, name):
        try:
            item = ItemModel.find_by_name(name)
            if item is None:
                return {"message": "The item does not exist"}
            item.remove()
        except:
            return{"message":"Error occur while removing an item"}, 500
        
        return {"message":f"Item {name} deleted"}, 204

    @jwt_required()
    def put(self, name): 
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data["price"])

        if item is None: 
            try:
                updated_item.insert()
            except:
                return{"message":"Error occur while inserting an item"}, 500            
        else:
            try:
                updated_item.update()
            except:
                return{"message":"Error occur while updating an item"}, 500

        return updated_item.json()
