from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from werkzeug.contrib.profiler import ProfilerMiddleware


app = Flask(__name__)
api = Api(app)

app.config.from_envvar('YOURAPPLICATION_SETTINGS')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['PROFILE'] = True
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
import generalstore.models as models

models.connect_to_db(app)

models.db.create_all()

import generalstore.resources as resources

print(app.config['SQLALCHEMY_DATABASE_URI'])
@app.before_first_request
def create_tables():
    models.db.create_all()


app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


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
api.add_resource(resources.ObjectManage, '/db/object/<o_type>')
api.add_resource(resources.Status, '/status')

# TODO: GET with OBJECT/TS filter
# TODO: GET with OBJECT Keys
# TODO: Verson based optimistic transaction commit
# TODO: Postgres migration
# TODO: Parent/Child in the same table
# TODO: UWSGI or similar and associated refactor!

if __name__ == "__main__":
    app.run()