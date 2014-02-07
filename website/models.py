from django.db import models
from openup import settings

def first_rank_higher(first, second):
    RANKS = [
        'Family', 'Subfamily', 'Genus', 'Species', 'Subspecies'
    ]
    
    return (RANKS.index(first) < RANKS.index(second))

class Family(models.Model):
    name = models.CharField(max_length=200)
    
    def count_pictures(self):
        return len(self.picture_set.all())

    class Meta:
        ordering = ["name"]
    
class Subfamily(models.Model):
    name = models.CharField(max_length=200)
    family = models.ForeignKey(Family, null=True, blank=True)   

class Genus(models.Model):
    name = models.CharField(max_length=200)
    family = models.ForeignKey(Family, null=True, blank=True)
    subfamily = models.ForeignKey(Subfamily, null=True, blank=True)

class Species(models.Model):
    name = models.CharField(max_length=200)
    family = models.ForeignKey(Family, null=True, blank=True)
    subfamily = models.ForeignKey(Subfamily, null=True, blank=True)
    genus = models.ForeignKey(Genus, null=True, blank=True )

class Subspecies(models.Model):
    name = models.CharField(max_length=200)
    family = models.ForeignKey(Family, null=True, blank=True)
    subfamily = models.ForeignKey(Subfamily, null=True, blank=True)
    genus = models.ForeignKey(Genus, null=True, blank=True )
    species = models.ForeignKey(Species, null=True, blank=True)
    
class ViewType(models.Model):
    name = models.CharField(max_length=200)    

class Country(models.Model):
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=200)
    
class Province(models.Model):
    name = models.CharField(max_length=200)
    
class Station(models.Model):
    name = models.CharField(max_length=200)    

# Create your models here.
class Picture(models.Model):
    scientificname = models.CharField(max_length=255)
    
    # Taxonomy     
    family = models.ForeignKey(Family)
    subfamily = models.ForeignKey(Subfamily, blank=True, null=True)
    genus = models.ForeignKey(Genus)
    species = models.ForeignKey(Species)
    subspecies = models.ForeignKey(Subspecies, blank=True, null=True)
    
    # Collect
    country = models.ForeignKey(Country, blank=True, null=True)
    province = models.ForeignKey(Province, blank=True, null=True)
    station = models.ForeignKey(Station, blank=True, null=True)
    
    # We keep eventdate as a string because original data is quite incorrect.
    # We'll add a second (interpreted) field if necessary
    eventdate_verbatim = models.CharField(max_length=20, blank=True, null=True)
    
    # Picture
    view = models.ForeignKey(ViewType)
    picture_id = models.IntegerField()
    fileuri = models.URLField()
    origpathname = models.CharField(max_length=200)
    
    # For search:returns the FK name based on the model we want
    # This FK is in use in the Picture table, but also in the different Taxon models (to reference the parent levels)
    # TODO: Make this dynamic ?
    model_fk_mapping = {
        'Family': 'family_id',
        'Genus': 'genus_id',
        'Species': 'species_id',
    }
    
    def formatted_fk_name(self, attribute_name):
        try:
            t = getattr(self, attribute_name)
            return t.name
        except AttributeError:
            return '/'

    @property
    def subfamily_name_formatted(self):
        return self.formatted_fk_name('subfamily')

    @property
    def family_name_formatted(self):
        return self.formatted_fk_name('family')

    @property
    def genus_name_formatted(self):
        return self.formatted_fk_name('genus')

    @property
    def species_name_formatted(self):
        return self.formatted_fk_name('species')

    @property
    def subspecies_name_formatted(self):
        return self.formatted_fk_name('subspecies')

    @property
    def country_name_formatted(self):
        return self.formatted_fk_name('country')

    @property
    def province_name_formatted(self):
        return self.formatted_fk_name('province')

    @property
    def station_name_formatted(self):
        return self.formatted_fk_name('station')

    @property
    def view_name_formatted(self):
        return self.formatted_fk_name('view')

    @property
    def fileuri_picture_only(self):
        # We derive it from the fileuri field
        uri = list(self.fileuri.rpartition('/'))
        uri[-2] = '/' + settings.PICTURES_ONLY_SUBFOLDER + '/'
        return "".join(uri)
        


