# -*- coding: utf-8 -*-
import sadisplay
import model


class TestDescribe(object):
    def test_single_mapper(self):

        objects, relations, inherits = sadisplay.describe([model.User])

        assert len(objects) == 1
        assert relations == []
        assert inherits == []
        assert objects[0] == {
            'name':
            model.User.__name__,
            'cols': [
                ('INTEGER', 'id', 'pk'),
                ('VARCHAR(50)', 'name', None),
            ],
            'indexes': [{
                'cols': ['name', 'department'],
                'name': 'ix_username_department',
            }],
            'props': [
                'address',
                'books',
            ],
            'methods': [
                'login',
            ],
        }

    def test_single_table(self):

        objects, relations, inherits = sadisplay.describe([model.notes])
        assert len(objects) == 1
        assert relations == []
        assert inherits == []

        assert objects[0] == {
            'name':
            model.notes.name,
            'cols': [
                ('INTEGER', 'id', 'pk'),
                ('INTEGER', 'user_id', 'fk'),
                ('VARCHAR(150)', 'body', None),
                ('VARCHAR(50)', 'name', None),
            ],
            'indexes': [{
                'cols': ['body'],
                'name': 'ix_notes_body'
            }, {
                'cols': ['name'],
                'name': 'ix_notes_name'
            }],
            'props': [],
            'methods': [],
        }

    def test_inherits(self):

        objects, relations, inherits = sadisplay \
            .describe([model.User, model.Admin, model.Manager])

        assert len(relations) == 0
        assert len(objects) == 3
        assert len(inherits) == 2
        assert objects[1] == {
            'name':
            model.Admin.__name__,
            'cols': [
                ('INTEGER', 'id', 'pk'),
                ('VARCHAR(50)', 'name', None),
                ('VARCHAR(50)', 'phone', None),
            ],
            'indexes': [{
                'cols': ['name', 'department'],
                'name': 'ix_username_department',
            }],
            'props': [
                'address',
                'books',
            ],
            'methods': [
                'permissions',
            ],
        }

        assert inherits[0] == {
            'child': model.Admin.__name__,
            'parent': model.User.__name__,
        }

    def test_relation(self):

        objects, relations, inherits = sadisplay \
            .describe([model.User, model.Address])

        assert len(objects) == 2
        assert objects[1] == {
            'name': model.Address.__name__,
            'cols': [
                ('INTEGER', 'id', 'pk'),
                ('INTEGER', 'user_id', 'fk'),
            ],
            'indexes': [],
            'props': ['user'],
            'methods': [],
        }

        assert len(inherits) == 0
        assert relations[0] == {
            'from': model.Address.__name__,
            'to': model.User.__name__,
            'by': 'user_id',
        }

    def test_table(self):

        objects, relations, inherits = sadisplay \
            .describe([model.Book])

        assert len(objects) == 1
        assert objects[0] == {
            'name':
            model.Book.__name__,
            'cols': [
                ('INTEGER', 'id', 'pk'),
                ('INTEGER', 'user_id', 'fk'),
                ('VARCHAR(50)', 'title', None),
            ],
            'indexes': [{
                'cols': ['title'],
                'name': 'ix_books_title',
            }],
            'props': ['user'],
            'methods': [],
        }

        objects, relations, inherits = sadisplay \
            .describe([model.Book, model.books])

        assert len(objects) == 1
        assert objects[0] == {
            'name':
            model.Book.__name__,
            'cols': [
                ('INTEGER', 'id', 'pk'),
                ('INTEGER', 'user_id', 'fk'),
                ('VARCHAR(50)', 'title', None),
            ],
            'indexes': [{
                'cols': ['title'],
                'name': 'ix_books_title',
            }],
            'props': ['user'],
            'methods': [],
        }

        objects, relations, inherits = sadisplay \
            .describe([model.books])

        assert len(objects) == 1
        assert objects[0] == {
            'name':
            model.books.name,
            'cols': [
                ('INTEGER', 'id', 'pk'),
                ('INTEGER', 'user_id', 'fk'),
                ('VARCHAR(50)', 'title', None),
            ],
            'indexes': [{
                'cols': ['title'],
                'name': 'ix_books_title',
            }],
            'props': [],
            'methods': [],
        }

    def test_column_property(self):

        objects, relations, inherits = sadisplay \
            .describe([model.Employee])

        assert len(objects) == 1
        assert objects[0] == {
            'name':
            model.Employee.__name__,
            'cols': [
                ('INTEGER', 'id', 'pk'),
                ('INTEGER', 'manager_id', 'fk'),
                ('VARCHAR(50)', 'name', None),
                ('VARCHAR(50)', 'rank', None),
            ],
            'indexes': [{
                'cols': ['name', 'department'],
                'name': 'ix_username_department',
            }],
            'props': ['address', 'books', 'department'],
            'methods': [],
        }
