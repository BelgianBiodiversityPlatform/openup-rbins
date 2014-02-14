# This command is used to load the "planches" data info the webapp.
#
# The planches data consists of pictures and an Excel file by Alain Drumont that match these
# filenames to existing Pictures. It should therefore be performed after loading the initial data.
#
# This script will currently not run on Heroku because it needs access to "local" source file.
# - Long term solution: adapt this script so it can read (XLS and images) from S3
# - Short term solution: fill database locally then use pgbackups to dump/restore this database to Heroku

import os
from optparse import make_option
from tempfile import gettempdir
import uuid

from xlrd import open_workbook
from PIL import Image

from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.core.management import call_command

from website.models import Picture, Planche

# Config
SHEET_NUM = 0  # Source data in first sheet
LINES_TO_SKIP = 3
EXISTING_PICTURE_FN_INDEX = 0
PLANCHE_FN_INDEX = 1
MISSING_EXTENSION = '.jpg'

JPG_QUALITY = 85


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (make_option('--truncate',
                                             action='store_true',
                                             dest='truncate',
                                             default=False,
                                             help='Remous previous Planches before loading'),)

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('You should provide the path to the source file as an argument.')
        else:
            if options['truncate']:
                self.stdout.write('Truncating previous data...\n')
                self._remove_all_plates()

            xls_path = args[0]
            self._import_xls_file(xls_path)
            self.stdout.write('\nDone.')

    def _remove_all_plates(self):
        # Remove models and main files...
        for p in Planche.objects.all():
            p.delete()  # Files will follow, thanks to signal in models.py

        # Remove sorl-thumbnail cache and thumbails...
        call_command('thumbnail', 'cleanup')
        call_command('thumbnail', 'clear')
        m = 'Thumbnails cleared: you may also need to restart dev. server and empty browser cache...'
        self.stdout.write(m)

    def _import_xls_file(self, source_path):
        self.stdout.write('Importing data from XLS...\n')
        self.stdout.write('Source file: %s...' % source_path)

        xls = open_workbook(source_path)
        
        sheet = xls.sheet_by_index(SHEET_NUM)
        for row_index in range(LINES_TO_SKIP, sheet.nrows):
            planche_raw_fn = sheet.cell(row_index, PLANCHE_FN_INDEX).value
            origpicture_raw_fn = sheet.cell(row_index, EXISTING_PICTURE_FN_INDEX).value
            self._import_planche(planche_raw_fn, origpicture_raw_fn, os.path.dirname(source_path))

    def _import_planche(self, planche_filename, original_picture_filename, xls_directory):
        # Planche are in the same dir than xls, missing file extensions...
        planche_path = os.path.join(xls_directory, planche_filename) + MISSING_EXTENSION
        existing_picture = Picture.objects.filter(origpathname__contains=original_picture_filename)

        # We try to reconcile existing images and planches
        if os.path.exists(planche_path) and len(existing_picture) == 1:
            # Ok, let's create a new Planche instance
            p = Planche()
            p.referenced_picture = existing_picture[0]
            p.planche_picture.save(planche_filename, self._prepare_planche_content(planche_path))
            p.save()

            self.stdout.write('.', ending="")
        else:
            tpl = 'Planche ({planche_path}) or existing pic. ({origpathname}) cannot be found.'
            self.stdout.write(tpl.format(planche_path=planche_path,
                                         origpathname=original_picture_filename))

    def _prepare_planche_content(self, original_planche_path):
        """ Takes a path to an initial plate and return an instance of django.cores.file.File.
         
        - output is ready to use by models.ImageField.
        - processing (resize, compress) may happen here.
        """
        im = Image.open(original_planche_path)
        tmp_path = os.path.join(gettempdir(), str(uuid.uuid4())) + '.jpg'
        im.save(tmp_path, quality=JPG_QUALITY)
        return File(open(tmp_path))

