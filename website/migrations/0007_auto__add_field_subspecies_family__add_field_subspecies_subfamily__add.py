# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Subspecies.family'
        db.add_column('website_subspecies', 'family',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Family'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Subspecies.subfamily'
        db.add_column('website_subspecies', 'subfamily',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Subfamily'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Subspecies.genus'
        db.add_column('website_subspecies', 'genus',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Genus'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Subspecies.species'
        db.add_column('website_subspecies', 'species',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Species'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Species.family'
        db.add_column('website_species', 'family',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Family'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Species.subfamily'
        db.add_column('website_species', 'subfamily',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Subfamily'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Species.genus'
        db.add_column('website_species', 'genus',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Genus'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Genus.subfamily'
        db.add_column('website_genus', 'subfamily',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Subfamily'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Subfamily.family'
        db.add_column('website_subfamily', 'family',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Family'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Subspecies.family'
        db.delete_column('website_subspecies', 'family_id')

        # Deleting field 'Subspecies.subfamily'
        db.delete_column('website_subspecies', 'subfamily_id')

        # Deleting field 'Subspecies.genus'
        db.delete_column('website_subspecies', 'genus_id')

        # Deleting field 'Subspecies.species'
        db.delete_column('website_subspecies', 'species_id')

        # Deleting field 'Species.family'
        db.delete_column('website_species', 'family_id')

        # Deleting field 'Species.subfamily'
        db.delete_column('website_species', 'subfamily_id')

        # Deleting field 'Species.genus'
        db.delete_column('website_species', 'genus_id')

        # Deleting field 'Genus.subfamily'
        db.delete_column('website_genus', 'subfamily_id')

        # Deleting field 'Subfamily.family'
        db.delete_column('website_subfamily', 'family_id')


    models = {
        'website.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'website.family': {
            'Meta': {'ordering': "['name']", 'object_name': 'Family'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'website.genus': {
            'Meta': {'object_name': 'Genus'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Family']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'subfamily': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Subfamily']", 'null': 'True', 'blank': 'True'})
        },
        'website.picture': {
            'Meta': {'object_name': 'Picture'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Country']", 'null': 'True', 'blank': 'True'}),
            'eventdate_verbatim': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Family']"}),
            'fileuri': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'genus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Genus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture_id': ('django.db.models.fields.IntegerField', [], {}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Province']", 'null': 'True', 'blank': 'True'}),
            'scientificname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Species']"}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Station']", 'null': 'True', 'blank': 'True'}),
            'subfamily': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Subfamily']", 'null': 'True', 'blank': 'True'}),
            'subspecies': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Subspecies']", 'null': 'True', 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.ViewType']"})
        },
        'website.province': {
            'Meta': {'object_name': 'Province'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'website.species': {
            'Meta': {'object_name': 'Species'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Family']", 'null': 'True', 'blank': 'True'}),
            'genus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Genus']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'subfamily': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Subfamily']", 'null': 'True', 'blank': 'True'})
        },
        'website.station': {
            'Meta': {'object_name': 'Station'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'website.subfamily': {
            'Meta': {'object_name': 'Subfamily'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Family']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'website.subspecies': {
            'Meta': {'object_name': 'Subspecies'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Family']", 'null': 'True', 'blank': 'True'}),
            'genus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Genus']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Species']", 'null': 'True', 'blank': 'True'}),
            'subfamily': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Subfamily']", 'null': 'True', 'blank': 'True'})
        },
        'website.viewtype': {
            'Meta': {'object_name': 'ViewType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['website']