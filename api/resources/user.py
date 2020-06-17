import json
from flask import request,redirect
from flask_restful import Resource, reqparse
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

import configurations
from models.user import UserModel

GOOGLE_CLIENT_ID = configurations.CLIENT_ID
GOOGLE_CLIENT_SECRET = configurations.CLIENT_SECRET
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

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


class UserLogin(Resource):

    def get(self):
         google_provider_cfg = get_google_provider_cfg()
         authorization_endpoint = google_provider_cfg["authorization_endpoint"]
         request_uri = client.prepare_request_uri(
         authorization_endpoint,
         redirect_uri=request.base_url + "/callback",
         scope=["openid", "email", "profile"],
        )

         return redirect(request_uri)

class UserLog(Resource):  
    def get(self):
         code = request.args.get("code")

         google_provider_cfg = get_google_provider_cfg()
         token_endpoint = google_provider_cfg["token_endpoint"]

         token_url, headers, body = client.prepare_token_request(
         token_endpoint,
         authorization_response=request.url,
         redirect_url=request.base_url,
         code=code
         )

         token_response = requests.post(
         token_url,
         headers=headers,
         data=body,
         auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
         )

         client.parse_request_body_response(json.dumps(token_response.json()))

         userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
         uri, headers, body = client.add_token(userinfo_endpoint)
         userinfo_response = requests.get(uri, headers=headers, data=body)

         if userinfo_response.json().get("email_verified"):
             unique_id = userinfo_response.json()["sub"]
             users_email = userinfo_response.json()["email"]
             users_name = userinfo_response.json()["given_name"]
         else:
             return "User email not available or not verified by Google.", 400

         print(type(unique_id))

         user = UserModel(unique_id,users_name,users_email)

         if not UserModel.find_by_id(unique_id):
             user.save_to_db()
        
         login_user(user)
         return redirect("/items") 





   