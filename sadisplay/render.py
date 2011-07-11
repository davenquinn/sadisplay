# -*- coding: utf-8 -*-
from sadisplay import __version__


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
