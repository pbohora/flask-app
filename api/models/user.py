from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    uid = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(80))
    # password = db.Column(db.String(80))

    def __init__(self, uid, username, email):
        self.uid = uid
        self.username = username
        self.email = email
        # self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()    

    @classmethod
    def find_by_id(cls, uid):
        return cls.query.filter_by(uid=uid).first()