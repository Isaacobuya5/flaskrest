import os

# from db import db
from security import authenticate, identity
from flask import Flask
# reqparse ensures we pass only certain
from flask_restful import Api
# set up jwt
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import ItemList, Item
from resources.store import Store, StoreList

app = Flask(__name__)
# specify config for sql alchemy
uri = os.environ.get('DATABASE_URL')
if uri:
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
else:
    uri = "sqlite:///data.db"

app.config['SQLALCHEMY_DATABASE_URI'] = uri

# turns flask SQLALCHEMY tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "isaac"  # consider using an environment variable
api = Api(app)

# tell SQLAlchemy to create table for you


# @app.before_first_request  # runs before any requests
# def create_tables():
#     db.create_all()


# JWT creates a new endpoint i.e. /auth -> username, and password required
jwt = JWT(app, authenticate, identity)

# items = []

# a resource must be a class and can only be retrieved with a get method

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

# prevent running the app upon import of the app file
if __name__ == '__main__':
    db.init_app(app)
    # debug=True returns a nice error page
    app.run(port=500, debug=True)
