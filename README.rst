Robeli Learning Platform
########################

Proprietary distribution based on internal Robeli components.

Purpose
*******
Robeli enables authoring and delivery of online learning at scale. The platform is built with Python, Django, and modern frontend tooling.

Documentation
*************
Internal docs: contact support@robeli.com for access.

Getting Started
***************

System Requirements
===================
- Ubuntu 24.04
- Python 3.11
- Node (see ``.nvmrc``)
- MySQL 8.0, MongoDB 7.x, Memcached

Install
=======
- Backend assets:

  - ``pip install -r requirements/edx/assets.txt``

- Backend application (development):

  - ``pip install -r requirements/edx/development.txt``

- Frontend:

  - ``npm clean-install --dev``
  - ``npm run build``

Database Setup
==============
Create the required databases and run migrations::

  ./manage.py lms migrate
  ./manage.py lms migrate --database=student_module_history
  ./manage.py cms migrate

Run Servers
===========
- LMS::

  ./manage.py lms runserver 18000

- CMS::

  ./manage.py cms runserver 18010

Branding
********
This distribution uses the `Robeli` theme. See ``themes/robeli/README.rst`` to customize colors, logos, and typography.

License
*******
This software is licensed under the Robeli Proprietary Software License. See ``LICENSE`` for details.

Support
*******
For assistance, email support@robeli.com.