# -*- coding: utf-8 -*-
from sadisplay import __version__

from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('sadisplay', 'templates'))

# by pull request
# https://bitbucket.org/estin/sadisplay/pull-requests/4/format-table-info/diff
def format_column(column):
    type, name, role = column
    role_char = {
        'pk': u'■',
        'fk': u'□',
    }.get(role, u' ')

    return type, name, '%s %s' % (role_char, name)


def format_index(index_name):
    type_char = u'\U000000BB'

    return '%s %s' % (type_char, index_name)


def format_index_type_string(index_columns):
    if not index_columns:
        return 'INDEX'

    indexes = ','.join(index_columns)
    return 'INDEX({0})'.format(indexes)


def format_property(property_name):
    type_char = u'\U000026AA'

    return '%s %s' % (type_char, property_name)


def tabular_output(table, indent=None, col_delimiter=None):
    indent = indent or ' ' * 4
    col_delimiter = col_delimiter or ' '
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table:
        yield indent + col_delimiter.join(u'{:{}}'.format(x, col_width[i])
                                          for i, x in enumerate(line))


def plantuml(desc):
    """Generate plantuml class diagram

    :param desc: result of sadisplay.describe function

    Return plantuml class diagram string
    """

    classes, relations, inherits = desc

    result = [
        '@startuml',
        'skinparam defaultFontName Courier',
    ]

    def _clean(v):
        return v.replace('(', '[').replace(')', ']')

    def _cleanup(col):
        type, name = col
        return _clean(type), name

    for cls in classes:
        # issue #11 - tabular output of class members (attrs)
        # http://stackoverflow.com/a/8356620/258194

        # build table
        class_desc = []
        # table columns
        class_desc += [_cleanup(format_column(i)) for i in cls['cols']]
        # class properties
        class_desc += [('+', i) for i in cls['props']]
        # methods
        class_desc += [('%s()' % i, '') for i in cls['methods']]
        # class indexes
        class_desc += [(_clean(format_index_type_string(i['cols'])),
                        format_index(i['name'])) for i in cls['indexes']]

        result.append('Class %(name)s {\n%(desc)s\n}' % {
            'name': cls['name'],
            'desc': '\n'.join(tabular_output(class_desc)),
        })

    for item in inherits:
        result.append("%(parent)s <|-- %(child)s" % item)

    for item in relations:
        result.append("%(from)s <--o %(to)s: %(by)s" % item)

    result += [
        'right footer generated by sadisplay v%s' % __version__,
        '@enduml',
    ]

    return '\n\n'.join(result)


def dot(desc):
    """Generate dot file

    :param desc: result of sadisplay.describe function

    Return string
    """

    classes, relations, inherits = desc

    result = []
    for cls in classes:
        template = env.get_template('column.html')
        cols = ' '.join([
            template.render(type=c[0], name=c[1], pretty_name=c[2])
            for c in map(format_column, cls['cols'])])


        ix_template = env.get_template('index.html')
        props = ' '.join([
            ix_template.render(
                name=format_property(p),
                type="PROPERTY"
            )  for p in cls['props']
        ])
        methods = ' '.join([
            ix_template.render(
                name=m,
                type="METHOD"
            ) for m in cls['methods']])

        indexes = ' '.join([
            template.render(
                name=format_index(i['name']),
                type=format_index_type_string(i['cols']),
            ) for i in cls['indexes']
        ])
        template = env.get_template('class.html')
        renderd = template.render(
            name=cls['name'],
            cols=cols,
            indexes=indexes,
            props=props,
            methods=methods)

        result.append(renderd)

    tpl = env.get_template("edges.html")
    result += [tpl.render(inherits=inherits,relations=relations)]

    _ = '\n'.join(result)

    return env.get_template("graph.dot").render(template=_)

