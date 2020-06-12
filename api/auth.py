from user import User

users = [
    User(1, "User1", "password1"),
    User(2, "User2", "password2")
]

username_table= {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and user.password==password:
        return user

def identity(payload):
    user_id = payload["identity"]
    return userid_table.get(user_id, None)