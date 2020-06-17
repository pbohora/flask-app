import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username", 
        type=str,
        required=True,
        help="Username is required!"
    )

    parser.add_argument("password", 
        type=str,
        required=True,
        help="password is required!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        print(UserModel.find_by_username(data["username"]))
        
        if UserModel.find_by_username(data["username"]):
            return {"message": "User already exists with that username"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "New user created"}, 201

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = "INSERT INTO users values (Null,?,?)"
        # cursor.execute(query,(data["username"], data["password"]))

        # connection.commit()
        # connection.close()

