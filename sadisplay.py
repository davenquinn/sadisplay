# -*- coding: utf-8 -*-
import types
from sqlalchemy.orm import class_mapper

def describe(mappers):
    """
    """

    objects = []
    relations = []
    inhirits = []

    for mapper in mappers:

        mapper = class_mapper(mapper)

        entry ={
            'name': mapper.class_.__name__,
            'attributes': [(col.type.__class__.__name__, col.name)
                    for col in mapper.columns],
            'methods': [],
        }

        for name, func in mapper.__dict__.iteritems():
            if isinstance(func, types.FunctionType):
                entry['methods'].append(name)

        objects.append(entry)

    return objects, relations, inhirits


def run():
    pass
