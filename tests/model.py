# -*- coding: utf-8 -*-
from sqlalchemy import Table, Column, Integer, Unicode, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, mapper


BASE = declarative_base()


class User(BASE):
    __tablename__ = 'user_table'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50))

    def login(self):
        pass

    def __repr__(self):
        pass


class Admin(User):
    __mapper_args__ = {'polymorphic_identity': 'admin'}

    phone = Column(Unicode(50))

    def permissions(self):
        pass

    def __unicode__(self):
        pass


class Manager(User):
    __mapper_args__ = {'polymorphic_identity': 'manager'}

    deparment = Column(Unicode(50))

    def permissions(self):
        pass

    def __unicode__(self):
        pass


class Address(BASE):
    __tablename__ = 'address_table'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_table.id'))
    user = relation(User, backref="address")


books = Table(
    'books',
    BASE.metadata,
    Column('id', Integer, primary_key=True),
    Column('title', Unicode(50), nullable=False),
    Column('user_id', Integer, ForeignKey('user_table.id')),
)


class Book(object):
    pass


mapper(Book, books, {'user': relation(User, backref='books')})


# Not mapped table
notes = Table(
    'notes',
    BASE.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(50), nullable=False),
    Column('user_id', Integer, ForeignKey('user_table.id')),
)
