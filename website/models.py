from django.db import models

class Family(models.Model):
    name = models.CharField(max_length=200)
    
class Subfamily(models.Model):
    name = models.CharField(max_length=200)    

class Genus(models.Model):
    name = models.CharField(max_length=200)

class Species(models.Model):
    name = models.CharField(max_length=200)

class Subspecies(models.Model):
    name = models.CharField(max_length=200)
    
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
    
    eventdate = models.DateField()
    
    # Picture
    view = models.ForeignKey(ViewType)
    picture_id = models.IntegerField()


