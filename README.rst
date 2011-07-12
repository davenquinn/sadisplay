.. -*- restructuredtext -*-

=========
sadisplay
=========

About
=====
Simple package for describing SQLAlchemy schema and display raw database
tables. Relation detecting by `ForeignKey` columns.
Supports mapped class inherit. BSD licensed.


Output formats:

 * `PlantUML <http://plantuml.sourceforge.net/>`_ class diagram
 * `DOT <http://www.graphviz.org/>`_ graphviz directed graphs


Requirements
============
 * python >= 2.5
 * SQLAlchemy >= 0.5


Install
=======

::

    pip install sadisplay

From bitbucket::

    pip install http://bitbucket.org/estin/sadisplay/get/tip.tar.gz
    # or
    easy_install http://bitbucket.org/estin/sadisplay/get/tip.tar.gz


Usage
=====

Write simple script in your project environment::

    import sadisplay
    from yourapp import model

    desc = sadisplay.describe([getattr(model, attr) for attr in dir(model)])
    open('schema.plantuml', 'w').write(sadisplay.plantuml(desc))

    # Or only part of schema
    desc = sadisplay.describe([model.User, model.Group, model.Persmission])
    open('auth.plantuml', 'w').write(sadisplay.plantuml(desc))



Render PlantUML class diagram::

    $ java -jar plantuml.jar schema.plantuml

    # or for svg format
    $ java -jar plantuml.jar -Tsvg schema.plantuml


Also you can display you sql database tables by reflecting feature::

    $ sadisplay -u <URL connection string to db> -r dot > schema.dot
    $ dot -Tpng schema.dot > schema.png
