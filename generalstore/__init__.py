from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# import generalstore.models

# db = SQLAlchemy()
# jwt = JWTManager()
# api = Api()

# def create_app(config_file):
#     app = Flask(__name__)
#     api = Api(app)
#     app.config.from_envvar('YOURAPPLICATION_SETTINGS')
#     # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['PROPAGATE_EXCEPTIONS'] = True
#     return api, app
#
#
# def initialize_extensions(app):
#     db = SQLAlchemy(app)
#     jwt = JWTManager(app)
#     app.config['JWT_BLACKLIST_ENABLED'] = True
#     app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
#     return db
#
# def register(app):
#     api.add_resource(resources.UserRegistration, '/registration')
#     api.add_resource(resources.UserLogin, '/login')
#     api.add_resource(resources.UserLogoutAccess, '/logout/access')
#     api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
#     api.add_resource(resources.TokenRefresh, '/token/refresh')
#     api.add_resource(resources.AllUsers, '/users')
#     api.add_resource(resources.SecretResource, '/secret')
#     api.add_resource(resources.ObventManage, '/db/<id>')
#


