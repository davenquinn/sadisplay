# -*- coding: utf-8 -*-
import uuid
import types
import locale
from functools import cmp_to_key

from sqlalchemy import exc, orm
from sqlalchemy.orm import class_mapper
from sqlalchemy import Column, Integer, Table
from sqlalchemy.orm.properties import ColumnProperty

try:
    # sa >= 0.9
    from sqlalchemy.sql.elements import Label
except ImportError:
    from sqlalchemy.sql.expression import Label


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
                (
                    '<Column type class name>',
                    '<Column name>',
                    '<pk|fk>',),
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

    def column_role(column):
        if column.primary_key:
            return 'pk'
        elif column.foreign_keys:
            return 'fk'

    def column_compare(a, b):
        if a[2] != 'pk' and b[2] == 'pk':
            return 1
        if a[2] == 'pk' and b[2] != 'pk':
            return -1
        return locale.strcoll(a[1], b[1])

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
                self.methods = mapper.class_.__dict__.items()
                self.inherits = mapper.inherits
                self.properties = mapper.iterate_properties
                self.bases = mapper.class_.__bases__
                self.class_ = mapper.class_
                self.table_name = str(mapper.mapped_table)

            elif table is not None:
                self.name = table.name
                self.table_name = table.name
                # prepend schema if exists for foreign key matching
                if hasattr(table, "schema") and table.schema:
                    self.table_name = table.schema + "." + self.table_name
                self.columns = table.columns
            else:
                pass

        def __repr__(self):
            return '<{s.__class__.__name__} {s.name}>'.format(s=self)

        def __eq__(self, other):
            if other.inherits or self.inherits:
                return self.name == other.name
            return self.table_name == other.table_name

    objects = []
    relations = []
    inherits = []

    entries = []
    for item in items:
        try:
            mapper = class_mapper(item)
        except (exc.ArgumentError, orm.exc.UnmappedClassError):
            if isinstance(item, Table):
                entity = EntryItem(table=item)
            else:
                continue
        else:
            entity = EntryItem(mapper=mapper)

        if entity not in entries:
            entries.append(entity)

    for entry in entries:

        result_item = {
            'name': entry.name,
            'cols': [
                (
                    str(col.type),
                    name,
                    column_role(col),
                ) for name, col in entry.columns.items()
                if not isinstance(col, Label)
            ],
            'props': [],
            'methods': [],
        }

        # sort columns by role and name
        result_item['cols'].sort(
            key=cmp_to_key(column_compare),
        )

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

                DummyClass = type('Dummy%s' % suffix, entry.bases, params)

                base_methods = DummyClass.__dict__.keys()

            # Filter mapper methods
            for name, func in entry.methods:
                if name[0] != '_' and name not in base_methods:
                    if isinstance(func, types.FunctionType):
                        result_item['methods'].append(name)

        if show_properties:

            # find relationship properties
            for item in entry.properties:
                if not isinstance(item, ColumnProperty):
                    result_item['props'].append(item.key)

            # find column_property() as sql expressions
            for name, item in entry.columns.items():
                if isinstance(item, Label):
                    result_item['props'].append(name)

        # ordering
        for key in ('methods', 'props'):
            result_item[key].sort()

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

            inh = {
                'child': entry.name,
                'parent': EntryItem(mapper=entry.inherits).name,
            }

            inherits.append(inh)

            # Delete relation by inherits
            for i, rel in enumerate(relations):
                if inh['child'] == rel['from'] and inh['parent'] == rel['to']:
                    relations.pop(i)

    return objects, relations, inherits
