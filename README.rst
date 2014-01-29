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