# -*- coding: utf-8 -*-
from sqlalchemy import Table, Column, Integer, Unicode, ForeignKey, Index
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
    __tablename__ = 'admin_table'
    __mapper_args__ = {'polymorphic_identity': 'user_table'}

    id = Column(Integer, ForeignKey('user_table.id'), primary_key=True)
    phone = Column(Unicode(50))

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
    Column('title', Unicode(200), nullable=False),
    Column('user_id', Integer, ForeignKey('user_table.id')), )

Index("ix_user_title", books.c.user_id, books.c.title)


class Book(object):
    pass


mapper(Book, books, {'user': relation(User, backref='books')})

# Not mapped table
notes = Table(
    'notes',
    BASE.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(200), nullable=False),
    Column('user_id', Integer, ForeignKey('user_table.id')), )

if __name__ == '__main__':
    import codecs
    import sadisplay

    desc = sadisplay.describe(globals().values())

    with codecs.open('/tmp/schema.plantuml', 'w', encoding='utf-8') as f:
        f.write(sadisplay.plantuml(desc))

    with codecs.open('/tmp/schema.dot', 'w', encoding='utf-8') as f:
        f.write(sadisplay.dot(desc))
