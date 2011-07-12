# -*- coding: utf-8 -*-
import uuid
import types
from sqlalchemy.orm import class_mapper, exc
from sqlalchemy import Column, Integer, Table
from sqlalchemy.orm.properties import PropertyLoader


def describe(items, show_methods=True, show_properties=True):
    """Detecting attributes, inherits and relations

    :param items: list of objects to describe
    :param show_methods: do detection of methods
    :param show_properties: do detection of properties

    Return tuple (objects, relations, inherits)


    Where objects is list::

        [{
            'name': '<Mapper class name or table name>',
            'cols': [
                ('<Column type class name>', '<Column name>'),
                ...
            ],
            'props': ['<Property name>'],
            'methods': ['<Method name>', ...],
        }, ...]


    Relations is::

        [{
            'from': '<From mapper class name>',
            'by': '<By mapper foreign key column name>',
            'to': '<To mapper class name>',
        }, ...]


    Example usage::

        import sadisplay
        from app import models

        desc = sadisplay.describe([
            getattr(model, attr) for attr in dir(model)
        ])

        desc = sadisplay.describe([models.User, models.Group])
    """

    class EntryItem(object):
        """Class adaptor for mapped classes and tables"""
        name = None
        methods = []
        columns = []
        inherits = None
        properties = []
        bases = tuple()

        def __init__(self, mapper=None, table=None):

            if mapper is not None:
                self.name = mapper.class_.__name__
                self.columns = mapper.columns
                self.methods = mapper.class_.__dict__.iteritems()
                self.inherits = mapper.inherits
                self.properties = mapper.iterate_properties
                self.bases = mapper.class_.__bases__
                self.class_ = mapper.class_
                self.table_name = unicode(mapper.mapped_table)

            elif table is not None:
                self.name = table.name
                self.table_name = table.name
                self.columns = table.columns
            else:
                pass

        def __eq__(self, other):
            return self.name == other

    objects = []
    relations = []
    inherits = []

    entries = []

    for item in items:
        try:
            entries.append(EntryItem(mapper=class_mapper(item)))
        except exc.UnmappedClassError:

            if isinstance(item, Table):
                # Filter if table mapper already appended
                if item.name not in [i.table_name for i in entries]:
                    entries.append(EntryItem(table=item))

    for entry in entries:

        result_item = {
            'name': entry.name,
            'cols': [(col.type.__class__.__name__, col.name)
                            for col in entry.columns],
            'props': [],
            'methods': [],
        }

        if show_methods and entry.methods:

            if entry.inherits:
                base_methods = entry.inherits.class_.__dict__.keys()
            else:
                # Create the DummyClass subclass of mapper bases
                # for detecting mapper own methods
                suffix = '%s' % str(uuid.uuid4())
                params = {
                    '__tablename__': 'dummy_table_%s' % suffix,
                    'dummy_id_col': Column(Integer, primary_key=True)
                }

                DummyClass = type('Dummy%s' % suffix,
                        entry.bases, params)

                base_methods = DummyClass.__dict__.keys()

            # Filter mapper methods
            for name, func in entry.methods:
                if name[0] != '_' and name not in base_methods:
                    if isinstance(func, types.FunctionType):
                        result_item['methods'].append(name)

        if show_properties and entry.properties:
            for loader in entry.properties:
                if isinstance(loader, PropertyLoader) \
                        and loader.mapper.class_.__name__ in entries:
                    result_item['props'].append(loader.key)

        objects.append(result_item)

        # Detect relations by ForeignKey
        for col in entry.columns:
            for fk in col.foreign_keys:
                table = fk.column.table
                for m in entries:
                    try:
                        if str(table) == str(m.table_name):
                            relations.append({
                                'from': entry.name,
                                'by': col.name,
                                'to': m.name,
                            })
                    except AttributeError:
                        pass

        if entry.inherits:
            inherits.append({
                'child': entry.name,
                'parent': EntryItem(mapper=entry.inherits).name,
            })

    return objects, relations, inherits
