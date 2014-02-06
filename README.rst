=========================
OpenUP RBINS Contribution
=========================

What is it ?
============

This repository contains all source code written in the context of helping the RBINS_ to publish its high-resolution beetles pictures to the OpenUP_ / Europeana_ project.

It consists of:
    * Data import/transformation scripts that are used to turn the original data (Excel files and high-resolution JPEG files) into usable data for OpenUP (to be served through BioCASE_)
    * The source code (Django_ project) of the website buld to showncase these pictures (http://projects.biodiversity.be/openuprbins/)

(Webapp) Requirements
=====================

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

(Webapp) Running locally
========================

To keep auto-reaload working:

::

    $ foreman run python manage.py runserver 0.0.0.0:5000

OR to ensure same running details than on heroku:

::

    $ foreman start


(Webapp) Deploy to staging
==========================

::

    $ git push heroku master


(Webapp) Install:
=================

$ python manage.py syncdb

Data import:
============

The data import process takes as input:

* Original, high resolution images (JPEG, with fancy filenames and sorted in different directories, by family).
* The Excel file managed by S. Kerkhof.

And will output:

* Transformed images that will be served on the web (two versions for each: one resized with just the animal, the other resized with additional overlays: scientific name, license info, ...).
* A database (referencing these images) to be used as a source for OpenUP_ publication (trough the BioCASE_ provider). The only really necessary output consists of "rbinsphotos" (consumed by BioCASE + website import) and rbinsmetadata views 
* Another database for the website (Django_ project).

Process overview:
-----------------

!!! Steps 1-3 are overly fragile and complex, but currently necessary as the CORRECT taxonomic data is not present in the Excel file and has to be extracted from file path/names !!!
!!! Notes for rewriting this process (and the related data requirements can be found in data_import_tools/import_review.rst)

1) data_import_tools/images_transformation/transform.rb resize the images, add overlays, some padding, ...
2) The Excel file and the result of an image directory "walk" are reconciled and imported in the "OpenUP" PostgreSQL database (will be consumed by BioCASE_ provider)
3) data_import_tools/images_transformation/step2/move_files.rb loop on the newly created rbinsphotos table, and for each row rename the associated image to <ROW_ID>.jpg and move it to a flat directory structure.
4) We publish these static files on the Internet
5) We use the a CSV dumpp of the "OpenUP" database to populate the "website" database.


Step 1: details
---------------

* Requires rmagick
* Configure constants in transform.rb

Step 2: details
---------------

* The OpenUP database is built using data_import_tools/create.sql
* This SQL script relies on 2 CSV data sources:
    * the main CSV file is just an export of the source Excel file (field separator: ; / encoding: UTF-8) !! You'll have to add a line column after remarks, containing the line number
    * walk.csv is generated using walk.rb (that walks over the images directory)
    

Step 5: details:
----------------

- We first extract data into CSV from Andre's view:

::  
  
    $ psql -h dev -U postgres -d openup_rbins
    openup_rbins=# COPY (SELECT * FROM rbinsphotos) TO 'openup_export.csv' WITH CSV HEADER;
  

- Load it into Django_:

::

    $ ./manage.py load_rbins_data data/openup_export.csv --truncate

.. _RBINS: http://www.naturalsciences.be/
.. _OpenUP: http://open-up.eu/
.. _Europeana: http://www.europeana.eu/
.. _BioCASE: http://www.biocase.org/
.. _Django: https://www.djangoproject.com/