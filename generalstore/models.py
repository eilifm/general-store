from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP, VARCHAR
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from passlib.hash import pbkdf2_sha256 as sha256
from flask import url_for, request
import _datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, CHAR
import uuid

db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to Flask app."""

    # Configure to use PostgreSQL database
    db.app = app
    db.init_app(app)


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class Obvents(db.Model):
    __tablename__ = 'obvents'
    id = db.Column(UUID, primary_key = True)
    last_ts = db.Column(TIMESTAMP, onupdate=_datetime.datetime.now(), server_default=db.func.current_timestamp(), server_onupdate=db.func.current_timestamp(), index=True)
    o_type = db.Column(VARCHAR(255), index=True)
    val = db.Column(JSONB)
    parent_id = db.Column(UUID, ForeignKey('obvents.id'), index=True)

    parent = relationship(lambda: Obvents, remote_side=id, backref='sub_regions')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'data': self.val,
            "o_type": self.o_type,
            "last_ts": self.last_ts.isoformat()
        }

    def add(self):
        db.session.add(self)
        db.session.commit()

    def save(self):
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()


    @classmethod
    def find_by_type(cls, o_type):
        page = request.args.get('page', 1, type=int)
        posts = cls.query.filter_by(o_type = o_type).order_by(Obvents.last_ts.desc()).paginate(
            page, 10, False)
        # posts = cls.query.filter_by(o_type = o_type).paginate(
        #     page, 10, False)
        next_url = url_for('objectmanage', o_type = o_type, page=posts.next_num) \
            if posts.has_next else None
        prev_url = url_for('objectmanage', o_type = o_type, page=posts.prev_num) \
            if posts.has_prev else None
        return posts, next_url, prev_url




