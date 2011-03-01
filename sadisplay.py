# -*- coding: utf-8 -*-
import types
from sqlalchemy.orm import class_mapper
from sqlalchemy import Column, Integer


def describe(mappers):
    """
    """

    objects = []
    relations = []
    inhirits = []

    for mapper in mappers:

        mapper = class_mapper(mapper)

        entry = {
            'name': mapper.class_.__name__,
            'attributes': [(col.type.__class__.__name__, col.name)
                            for col in mapper.columns],
            'methods': [],
        }

        # Create the DummyClass subclass of mapper bases
        # for detecting mapper own methods
        DummyClass = type('Dummy%s' % mapper.class_.__name__,
            mapper.class_.__bases__, {
                '__tablename__': 'dummy_table_%s' % mapper.class_.__name__,
                '__dummy_col': Column(Integer, primary_key=True)
            }
        )

        base_keys = DummyClass.__dict__.keys()

        for name, func in mapper.class_.__dict__.iteritems():
            if name not in base_keys:
                if isinstance(func, types.FunctionType):
                    entry['methods'].append(name)

        objects.append(entry)

    return objects, relations, inhirits
