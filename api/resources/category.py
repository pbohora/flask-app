from flask_restful import Resource
from models.category import CategoryModel

class Category(Resource):
    def get(self,name):
        category = CategoryModel.find_by_name(name)
        if category:
            return category.json()
        return {"message":"Category not found"}, 404


    def post(self,name):
        category = CategoryModel.find_by_name(name)
        if category:
            return {"message":f"A category with name {name} already exists"}, 400
        
        category = CategoryModel(name)
        try:
            category.save_to_db()
        except:
            return {"message": "An error occured while creating category"}, 500

        return category.json(), 201

    def delete(self,name):
        category = CategoryModel.find_by_name(name)
        if category:
            category.remove_from_db()
        return {"message":"category deleted"}, 204


class CategoryList(Resource):
    def get(self):
        return {"categories" : [category.json() for category in CategoryModel.query.all()]}