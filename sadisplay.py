# -*- coding: utf-8 -*-
import uuid
import types
from sqlalchemy.orm import class_mapper, exc
from sqlalchemy import Column, Integer
from sqlalchemy.orm.properties import PropertyLoader


__version__ = '0.3dev'


def describe(items, show_methods=True, show_properties=True):
    """Detecting mapper attributes, inherits and relations

    :param items: list of mappers to describe
    :param show_methods: do detection of methods
    :param show_properties: do detection of properties

    Return tuple (objects, relations, inherits)


    Where objects is list::

        [{
            'name': '<Mapper class name>',
            'cols': [
                ('<Mapper column type class name>', '<Mapper column name>'),
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

    objects = []
    relations = []
    inherits = []

    mappers = []

    for item in items:
        try:
            mappers.append(class_mapper(item))
        except exc.UnmappedClassError:
            from sqlalchemy.orm import mapper
            # create mapper
            dummy_class = type(item.name, tuple(), {})
            #dummy_class = object()
            mapper(dummy_class, item, {})
            mappers.append(class_mapper(dummy_class))
        except:
            pass


    for mapper in mappers:

        entry = {
            'name': mapper.class_.__name__,
            'cols': [(col.type.__class__.__name__, col.name)
                            for col in mapper.columns],
            'props': [],
            'methods': [],
        }

        if show_methods:

            if mapper.inherits:
                base_methods = mapper.inherits.class_.__dict__.keys()
            else:
                # Create the DummyClass subclass of mapper bases
                # for detecting mapper own methods
                suffix = '%s' % str(uuid.uuid4())
                params = {
                    '__tablename__': 'dummy_table_%s' % suffix,
                    'dummy_id_col': Column(Integer, primary_key=True)
                }

                DummyClass = type('Dummy%s' % suffix,
                        mapper.class_.__bases__, params)

                base_methods = DummyClass.__dict__.keys()

            # Filter mapper methods
            for name, func in mapper.class_.__dict__.iteritems():
                if name[0] != '_' and name not in base_methods:
                    if isinstance(func, types.FunctionType):
                        entry['methods'].append(name)

        if show_properties:
            for loader in mapper.iterate_properties:
                if isinstance(loader, PropertyLoader) \
                        and loader.mapper in mappers:
                    entry['props'].append(loader.key)

        objects.append(entry)

        # Detect relations by ForeignKey
        for col in mapper.columns:
            for fk in col.foreign_keys:
                table = fk.column.table
                for m in mappers:
                    try:
                        if str(table) == str(m.mapped_table.name):
                            relations.append({
                                'from': mapper.class_.__name__,
                                'by': col.name,
                                'to': m.class_.__name__,
                            })
                    except AttributeError:
                        pass

        if mapper.inherits:
            inherits.append({
                'child': mapper.class_.__name__,
                'parent': mapper.inherits.class_.__name__,
            })

    return objects, relations, inherits


def plantuml(desc):
    """Generate plantuml class diagram

    :param desc: result of sadisplay.describe function

    Return plantuml class diagram string
    """

    classes, relations, inherits = desc

    CLASS_TEMPLATE = "Class %(name)s {\n%(cols)s\n%(props)s\n%(methods)s\n}\n"

    COLUMN_TEMPLATE = "\t%(type)s \t\t%(name)s"

    PROPERTY_TEMPLATE = "\t+\t\t%(name)s"

    METHOD_TEMPLATE = "\t%(name)s()"

    INHERIT_TEMPLATE = "%(parent)s <|-- %(child)s\n"

    RELATION_TEMPLATE = "%(from)s <--o %(to)s: %(by)s\n"

    result = ['@startuml']

    for cls in classes:
        renderd = CLASS_TEMPLATE % {
                'name': cls['name'],
                'cols': '\n'.join([
                    COLUMN_TEMPLATE % {'type': c[0], 'name': c[1]}
                        for c in cls['cols']
                ]),
                'props': '\n'.join([
                    PROPERTY_TEMPLATE % {'name': p}
                        for p in cls['props']
                ]),
                'methods': '\n'.join([
                    METHOD_TEMPLATE % {'name': m}
                        for m in cls['methods']
                ]),
            }

        result.append(renderd)

    for item in inherits:
        result.append(INHERIT_TEMPLATE % item)

    for item in relations:
        result.append(RELATION_TEMPLATE % item)

    result += [
        'right footer sadisplay v%s' % __version__,
        '@enduml',
    ]

    return '\n'.join(result)


def dot(desc):
    """Generate dot file

    :param desc: result of sadisplay.describe function

    Return string
    """

    classes, relations, inherits = desc

    CLASS_BODY = "\n\t\tlabel=\"{%(name)s|%(cols)s|%(props)s|%(methods)s\l}\""
    CLASS_TEMPLATE = "\t%(name)s [" + CLASS_BODY + "\n\t]\n"

    COLUMN_TEMPLATE = "\t%(type)s \t\t%(name)s\l"

    PROPERTY_TEMPLATE = "\t%(name)s\l"

    METHOD_TEMPLATE = "\t%(name)s()\l"

    EDGE_INHERIT = "\tedge [\n\t\tarrowhead = empty\n\t]"
    INHERIT_TEMPLATE = "\t%(child)s -> %(parent)s \n"

    EDGE_REL = "\tedge [\n\t\tarrowhead = ediamond\n\t\tarrowtail = open\n\t]"
    RELATION_TEMPLATE = "\t%(from)s -> %(to)s [taillabel = \"%(by)s\"]"

    result = ["""digraph G {
\tfontname = "Bitstream Vera Sans"
\tfontsize = 8

\tnode [
\t\tfontname = "Bitstream Vera Sans"
\t\tfontsize = 8
\t\tshape = "record"
\t]

\tedge [
\t\tfontname = "Bitstream Vera Sans"
\t\tfontsize = 8
\t]"""]

    for cls in classes:
        renderd = CLASS_TEMPLATE % {
                'name': cls['name'],
                'cols': ' '.join([
                    COLUMN_TEMPLATE % {'type': c[0], 'name': c[1]}
                        for c in cls['cols']
                ]),
                'props': ' '.join([
                    PROPERTY_TEMPLATE % {'name': p}
                        for p in cls['props']
                ]),
                'methods': ' '.join([
                    METHOD_TEMPLATE % {'name': m}
                        for m in cls['methods']
                ]),
            }

        result.append(renderd)

    result += [EDGE_INHERIT]
    for item in inherits:
        result.append(INHERIT_TEMPLATE % item)

    result += [EDGE_REL]
    for item in relations:
        result.append(RELATION_TEMPLATE % item)

    result += [
        '}'
    ]

    return '\n'.join(result)
