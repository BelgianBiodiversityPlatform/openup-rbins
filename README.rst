Requirements
============

The application requires the following environment variables to run:

* SECRET_KEY  # http://www.miniwebtool.com/django-secret-key-generator/

* GOOGLE_ANALYTICS_APP_NAME  # Something like UA-XXXXXX
* GOOGLE_ANALYTICS_USER_EMAIL
* GOOGLE_ANALYTICS_USER_PASS
* GOOGLE_ANALYTICS_TABLE_ID  #something like ga:123456

Running locally
===============

To keep auto-reaload working:

::

    $ foreman run python manage.py runserver 0.0.0.0:5000

OR to ensure same running details than on heroku:

::

    $ foreman start


Deploy to staging
=================

::

    $ git push heroku master


Install:
========

$ python manage.py syncdb

Data import:
============

- We first extract data into CSV from Andre's view:
  
  $ psql -h dev -U postgres -d openup_rbins
  openup_rbins=# COPY (SELECT * FROM rbinsphotos) TO '/Users/nicolasnoe/Dropbox/BBPF/websites/openup/openup/data/rbinsphotos.csv' WITH CSV HEADER;
  
- Load it into the app  
  $ ./manage.py load_rbins_data data/rbinsphotos.csv --truncate