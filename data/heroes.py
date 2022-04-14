import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class Hero(SqlAlchemyBase, UserMixin):
    __tablename__ = 'heroes'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String,
                              unique=True, primary_key=True)
    farm = sqlalchemy.Column(sqlalchemy.Integer)
    time = sqlalchemy.Column(sqlalchemy.Integer)
    meta = sqlalchemy.Column(sqlalchemy.Integer)
    front = sqlalchemy.Column(sqlalchemy.Integer)
    lane = sqlalchemy.Column(sqlalchemy.Integer)
    active_sup = sqlalchemy.Column(sqlalchemy.Integer)
