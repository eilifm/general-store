from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager



app = Flask(__name__)
api = Api(app)

app.config.from_envvar('YOURAPPLICATION_SETTINGS')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

# @app.errorhandler(jwt_extended_exception.NoAuthorizationError)
# def handle_auth_error(e):
#     return {'message': str(e)}, 401
#


import models

import resources

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)



api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')
api.add_resource(resources.ObventManage, '/db/<id>')

# TODO: GET with OBJECT/TS filter
# TODO: GET with OBJECT Keys
# TODO: Verson based optimistic transaction commit
# TODO: Postgres migration
# TODO: Parent/Child in the same table
# TODO: UWSGI or similar and associated refactor!

if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    api.run()