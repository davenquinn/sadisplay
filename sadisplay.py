# -*- coding: utf-8 -*-
import uuid
import types
from sqlalchemy.orm import class_mapper
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm.properties import PropertyLoader


def describe(mappers, methods=True):
    """
    """

    objects = []
    relations = []
    inherits = []

    for mapper in mappers:

        mapper = class_mapper(mapper)

        entry = {
            'name': mapper.class_.__name__,
            'attributes': [(col.type.__class__.__name__, col.name)
                            for col in mapper.columns],
            'methods': [],
        }

        if methods:

            suffix = '%s' % str(uuid.uuid4())

            # Create the DummyClass subclass of mapper bases
            # for detecting mapper own methods

            params = {'__tablename__': 'dummy_table_%s' % suffix}

            if mapper.inherits:
                params['__mapper_args__'] = {'polymorphic_identity':
                        mapper.inherits.class_.__tablename__}

                # Get primary key
                pk = [col for col in mapper.columns if col.primary_key]

                # ForeignKey for inherited class
                params['dummy_id_col'] = Column(pk[0].type,
                        ForeignKey(pk[0]), primary_key=True)
            else:
                params['dummy_id_col'] = Column(Integer, primary_key=True)

            DummyClass = type('Dummy%s' % suffix,
                    mapper.class_.__bases__, params)

            base_keys = DummyClass.__dict__.keys()

            # Filter mapper methods
            for name, func in mapper.class_.__dict__.iteritems():
                if name not in base_keys:
                    if isinstance(func, types.FunctionType):
                        entry['methods'].append(name)

        objects.append(entry)

        for loader in mapper.iterate_properties:
            if isinstance(loader, PropertyLoader) and loader.mapper in mappers:
                if hasattr(loader, 'reverse_property'):
                    relations.add(frozenset([loader, loader.reverse_property]))
                else:
                    relations.add(frozenset([loader]))

        if mapper.inherits:
            inherits.append({
                'child': mapper.class_.__name__,
                'parent': mapper.inherits.class_.__name__,
            })

    return objects, relations, inherits
