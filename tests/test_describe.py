# -*- coding: utf-8 -*-
import unittest

from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base

import sadisplay


class TestDescribe(unittest.TestCase):

    def setUp(self):
        self.BASE = declarative_base()


    def test_single(self):

        class User(self.BASE):
            __tablename__ = 'user_table'

            id = Column(Integer, primary_key=True)
            name = Column(Unicode(50))

            def login(self):
                pass

        objects, relations, inhirets = sadisplay.describe([User])

        assert len(objects) == 1
        assert relations == []
        assert inhirets == []
        assert objects[0] == {
                'name': User.__name__,
                'attributes': [('Integer', 'id'), ('Unicode', 'name')],
                'methods': ['login'],
            }


if __name__ == '__main__':
    unittest.main()
