# -*- coding: utf-8 -*-
"""
Program for generating plantuml or dot format
of a database tables by connection string

\n\nDatabase connection string - http://goo.gl/3GpnE
"""

from optparse import OptionParser
from sqlalchemy import create_engine, MetaData
from sadisplay import describe, render, __version__


def run():
    """Command for reflection database objects"""
    parser = OptionParser(version=__version__,
        description=__doc__)

    parser.add_option('-u', '--url', dest='url',
                    help='Database URL (connection string)')

    parser.add_option('-r', '--render', dest='render', default='plantuml',
                    choices=['plantuml', 'dot'],
                    help='Output format - plantuml or dot')

    (options, args) = parser.parse_args()

    if not options.url:
        print '-u/--url option required'
        exit(1)

    engine = create_engine(options.url, pool_size=5, max_overflow=0)
    meta = MetaData()

    meta.reflect(bind=engine)

    desc = describe(meta.tables.values())
    print getattr(render, options.render)(desc)
