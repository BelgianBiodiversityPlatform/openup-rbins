import csv
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from website.models import Picture, Family, Subfamily, Genus, Species, Subspecies, ViewType, Country, Province, Station

CSV_DELIMITER = ','
LINES_TO_SKIP = 1

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--truncate',
            action='store_true',
            dest='truncate',
            default=False,
            help='Truncate existing data tables before loading data.'),
        )
    
    def handle(self, *args, **options):
        source_csv_path = args[0]
        
        if options['truncate']:
            self.stdout.write('Truncating tables to get rid of previous data...\n')
            self._truncate_existing_tables()
            
        self._import_csv_file(source_csv_path)    
    
    def _import_csv_file(self, source_path):
        self.stdout.write('Importing data from CSV...\n')
        self.stdout.write('Source file: %s...' % source_path)
        
        try:
            reader = csv.DictReader(open(source_path, 'rb'), delimiter=CSV_DELIMITER)
            self.stdout.write('DONE\n')
        except IOError:
            raise CommandError('unable to open the source file ("%s"). Please check the usual suspects (path, readability, ...).' % source_path)
        
            self.stdout.write('Importing data...\n')

        # Process each row
        for row in reader:
            self.stdout.write('.')
            self.stdout.flush()
            
            self._parse_and_insert_row(row)
        
        self.stdout.write('DONE.\n')
        
    def _parse_and_insert_row(self, row):
        # row is a dictionary (automagically created from CSV headers!)
        p = Picture()
        
        # CSV/Model mappings
        p.scientificname = row['scientificname']
        p.eventdate_verbatim = row['eventdate']
        p.picture_id = row['unitid']
        p.fileuri = row['fileuri']
        
        # Some date will be stored in other tables...
        p.family = self._create_or_return_obj_by_name(Family, row['family'])
        p.subfamily = self._create_or_return_obj_by_name(Subfamily, row['subfamily'])
        p.genus = self._create_or_return_obj_by_name(Genus, row['genus'])
        p.species = self._create_or_return_obj_by_name(Species, row['species'])
        p.subspecies = self._create_or_return_obj_by_name(Subspecies, row['subspecies'])
        
        p.country = self._create_or_return_obj_by_name(Country, row['country'])
        p.province = self._create_or_return_obj_by_name(Province, row['province'])
        p.station = self._create_or_return_obj_by_name(Station, row['station'])
        
        p.view = self._create_or_return_obj_by_name(ViewType, row['view'])
        
        p.save()  
            
    def _create_or_return_obj_by_name(self, model, obj_name):
        """ Returns the instance of model where name match obj_name. If inexistent, instances are created on the fly. """
        
        if obj_name == '':
            return None
        
        try:
            instance = model.objects.get(name = obj_name)
        except ObjectDoesNotExist:
            # If such an instance doesn't exists, let's create one
            instance = model()
            instance.name = obj_name
            instance.save()
        
        return instance
        
    
    def _truncate_existing_tables(self):
        models_to_truncate = [Picture, Family, Subfamily, Genus, Species, Subspecies, ViewType, Country, Province, Station]
        for model in models_to_truncate:
            self.stdout.write('Truncating %s model. \n' % str(model))
            model.objects.all().delete()