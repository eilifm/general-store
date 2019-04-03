from flask_restful import Resource, reqparse, request
from generalstore.models import UserModel, RevokedTokenModel, Obvents, db
import datetime
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import json
from sqlalchemy import update
import sqlalchemy.exc as sq_exc



parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'msg': 'User {} already exists'.format(data['username'])}

        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password'])
        )

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'msg': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        except:
            return {'msg': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'msg': 'User {} doesn\'t exist'.format(data['username'])}

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'msg': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'msg': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'msg': 'Access token has been revoked'}
        except:
            return {'msg': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'msg': 'Refresh token has been revoked'}
        except:
            return {'msg': 'Something went wrong'}, 500



class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {
            'answer': 42
        }

obvent_parser = reqparse.RequestParser()
obvent_parser.add_argument('o_type', help = 'This field cannot be blank', required = True)
obvent_parser.add_argument('data', help = 'This field cannot be blank', required = True)


class ObventManage(Resource):
    @jwt_required
    def get(self, id):
        record = Obvents.find_by_id(id)
        if not record:
            return {'msg': 'record with id: {} not found'.format(id)}, 422
        else:
            return record.serialize

    def put(self, id):

        data = request.get_json(silent=True)
        if not data:
            try:
                data = json.loads(request.data)
            except json.JSONDecodeError:
                return {'msg': 'Something went wrong'}, 500
            return {'msg': 'Something went wrong'}, 500


        rows = db.session.query(Obvents).filter(Obvents.id == id).update(dict(val=data['data'], o_type=data['o_type'], last_ts=datetime.datetime.utcnow()))
        db.session.commit()
        if rows == 0:
            try:
                new_event = Obvents(id=id, val=data['data'], o_type=data['o_type'], o_id=data['o_id'])
            except KeyError:
                new_event = Obvents(id=id, val=data['data'], o_type=data['o_type'], o_id=None)

            try:
                new_event.add()
                return {"success": True}
            except sq_exc.IntegrityError as e:
                return {'msg': str(e)}, 403

            except Exception as e:
                print(type(e))
                return {'msg': "Something went wrong"}

        else:
            return {"success": True}
        # exist_obvent = Obvents.find_by_id(id)

        # if exist_obvent:
        #     exist_obvent.val = data['data']
        #     exist_obvent.o_type = data['o_type']
        #     exist_obvent.last_ts = datetime.datetime.utcnow()
        #     # exist_obvent.save()
        #     return exist_obvent.serialize
        #
        # else:
        #     try:
        #         new_event = Obvents(id=id, val=data['data'], o_type=data['o_type'], o_id=data['o_id'])
        #     except KeyError:
        #         new_event = Obvents(id=id, val=data['data'], o_type=data['o_type'], o_id=None)
        #
        #     try:
        #         new_event.add()
        #         return {"success": True}
        #     except sq_exc.IntegrityError as e:
        #         return {'msg': str(e)}, 403
        #
        #     except Exception as e:
        #         print(type(e))
        #         return {'msg': "Something went wrong"}

    # def post(self, id):
    #
    #     data = request.get_json(silent=True)
    #     if not data:
    #         try:
    #             data = json.loads(request.data)
    #         except json.JSONDecodeError:
    #             return {'msg': 'Something went wrong'}, 500
    #         return {'msg': 'Something went wrong'}, 500
    #
    #
    #     rows = db.session.query(Obvents).filter(Obvents.id == id).update(dict(val=data['data'], o_type=data['o_type'], last_ts=datetime.datetime.utcnow()))
    #     db.session.commit()
    #     if rows == 0:
    #         try:
    #             new_event = Obvents(id=id, val=data['data'], o_type=data['o_type'], o_id=data['o_id'])
    #         except KeyError:
    #             new_event = Obvents(id=id, val=data['data'], o_type=data['o_type'], o_id=None)
    #
    #         try:
    #             new_event.add()
    #             return {"success": True}
    #         except sq_exc.IntegrityError as e:
    #             return {'msg': str(e)}, 403
    #
    #         except Exception as e:
    #             print(type(e))
    #             return {'msg': "Something went wrong"}
    #
    #     else:
    #         return {"success": True}
    #

# class ObjectManage(Resource):
#     # @jwt_required
#     def get(self, o_type):
#         recs, next, prev = Obvents.find_by_type(o_type)
#         if not prev:
#             prev = ''
#         return { 'next': request.url_root[0:-1] + next,
#                  'last': request.url_root[0:-1] + prev,
#                  # 'last': request.base_url + prev,
#                  'data': [x.serialize for x in recs.items]
#                  }


class ObjectManage(Resource):
    @jwt_required
    def get(self, o_type):
        recs, next_url, prev = Obvents.get_last(o_type, request.args.get("n", type=int))

        if not prev:
            prev = ''
        else:
            prev = request.url_root[0:-1] + prev

        if not next_url:
            next_url = ''
        else:
            next_url = request.url_root[0:-1] + next_url
        return { 'next': next_url,
                 'last': prev,
                 'data': [x.serialize for x in recs.items]
                 }


class Status(Resource):
    def get(self):
        return {"success": True}
