# -*- coding: utf-8 -*-
import unittest
import sadisplay
import model


class TestDescribe(unittest.TestCase):

    def test_single(self):

        objects, relations, inherits = sadisplay.describe([model.User])

        assert len(objects) == 1
        assert relations == []
        assert inherits == []
        assert objects[0] == {
                'name': model.User.__name__,
                'attributes': [('Integer', 'id'), ('Unicode', 'name'), ],
                'methods': ['login', ],
            }

    def test_inherits(self):

        objects, relations, inherits = sadisplay \
                .describe([model.User, model.Admin])

        assert len(objects) == 2
        assert len(inherits) == 1
        assert objects[1] == {
                'name': model.Admin.__name__,
                'attributes': [('Integer', 'id'),
                    ('Unicode', 'name'),
                    ('Unicode', 'phone'), ],
                'methods': ['permissions', ],
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
                'attributes': [('Integer', 'id'), ('Integer', 'user_id'), ],
                'methods': [],
            }

        assert len(inherits) == 0
        assert relations[0] == {
                'from': model.Address.__name__,
                'to': model.User.__name__,
                'by': 'user_id',
            }


if __name__ == '__main__':
    unittest.main()
