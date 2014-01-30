=========================
OpenUP RBINS Contribution
=========================

What is it ?
============

This repository contains all source code written in the context of helping the RBINS_ to publish its high-resolution beetles pictures to the OpenUP_ / Europeana_ project.

It consists of:
    * Data import/transformation scripts that are used to turn the original data (Excel files and high-resolution JPEG files) into usable data for OpenUP (to be served through BioCASE_)
    * The source code (Django_ project) of the website buld to showncase these pictures (http://projects.biodiversity.be/openuprbins/)

Requirements
============

Required Python packages are listed in requirements.txt, install with:

::

    $ pip install -r requirements.txt


The application requires the following environment variables to run:

* DATABASE_URL  # postgres://username:password@host:port/db_name
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

The data import process takes as input:

* Original, high resolution images (JPEG, with fancy filenames and sorted in different directories, by family).
* The Excel file managed by S. Kerkhof.

And will output:

* Transformed images that will be served on the web (two versions for each: one resized with just the animal, the other resized with additional overlays: scientific name, license info, ...).
* A database (referencing these images) to be used as a source for OpenUP_ publication (trough the BioCASE_ provider).
* Another database for the website (Django_ project).

Process overview:
-----------------

1) data_import_tools/images_transformation/transform.rb resize the images, add overlays, some padding, ...
2) The Excel file is imported in the "OpenUP" PostgreSQL database (will be consumed by BioCASE_ provider)
3) data_import_tools/images_transformation/step2/move_files.rb loop on the newly created rbinsphotos table, and for each row rename the associated image to <ROW_ID>.jpg and move it to a flat directory structure.
4) We publish these static files on the Internet
5) We use the "OpenUP" database to populate the "website" database.


Step 5, in details:
-------------------

- We first extract data into CSV from Andre's view:

::  
  
    $ psql -h dev -U postgres -d openup_rbins
    openup_rbins=# COPY (SELECT * FROM rbinsphotos) TO '/Users/nicolasnoe/Dropbox/BBPF/websites/openup/openup/data/rbinsphotos.csv' WITH CSV HEADER;
  

- Load it into Django_:

::

    $ ./manage.py load_rbins_data data/rbinsphotos.csv --truncate

.. _RBINS: http://www.naturalsciences.be/
.. _OpenUP: http://open-up.eu/
.. _Europeana: http://www.europeana.eu/
.. _BioCASE: http://www.biocase.org/
.. _Django: https://www.djangoproject.com/