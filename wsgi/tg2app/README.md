Trine
=====

Trine in python mvc turbogears with sqlalchemy, jinja2 and cool Angular.

Installation and Setup
======================

Install ``trine`` using the setup.py script::

    $ cd trine/wsgi/tg2app
    $ python setup.py develop

Parameter *develop* is the key in this step. We do not want to install ``trine`` as regular package, but we just only need to install all dependencies.

Create the project database (if not exists, otherwise use gearbox migrate) for any model classes defined::

    $ gearbox setup-app


Start the paste http server::

    $ gearbox serve

While developing you may want the server to reload after changes in package files (or its dependencies) are saved. This can be achieved easily by adding the --reload option::

    $ gearbox serve --reload --debug

Then you are ready to go.
