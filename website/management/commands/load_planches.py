# This command is used to load the "planches" data info the webapp.
#
# The planches data consists of pictures and an Excel file by Alain Drumont that match these
# filenames to existing Pictures. It should therefore be performed after loading the initial data.
import os

from xlrd import open_workbook

from django.core.management.base import BaseCommand, CommandError
from django.core.files import File

from website.models import Picture, Planche

# Config
SHEET_NUM = 0  # Source data in first sheet
LINES_TO_SKIP = 3
EXISTING_PICTURE_FN_INDEX = 0
PLANCHE_FN_INDEX = 1
MISSING_EXTENSION = '.jpg'


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('You should provide the path to the source file as an argument.')
        else:
            xls_path = args[0]
            self._import_xls_file(xls_path)
            self.stdout.write('\nDone.')

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
            p.planche_picture.save(planche_filename, File(open(planche_path)))
            p.save()

            self.stdout.write('.', ending="")
        else:
            tpl = 'Planche ({planche_path}) or existing pic. ({origpathname}) cannot be found.'
            self.stdout.write(tpl.format(planche_path=planche_path,
                                         origpathname=original_picture_filename))

