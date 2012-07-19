# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Family'
        db.create_table('website_family', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('website', ['Family'])

        # Adding model 'Subfamily'
        db.create_table('website_subfamily', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('website', ['Subfamily'])

        # Adding model 'Genus'
        db.create_table('website_genus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('website', ['Genus'])

        # Adding model 'Species'
        db.create_table('website_species', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('website', ['Species'])

        # Adding model 'Subspecies'
        db.create_table('website_subspecies', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('website', ['Subspecies'])

        # Adding model 'ViewType'
        db.create_table('website_viewtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('website', ['ViewType'])

        # Adding model 'Country'
        db.create_table('website_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('website', ['Country'])

        # Adding model 'Province'
        db.create_table('website_province', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('website', ['Province'])

        # Adding model 'Station'
        db.create_table('website_station', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('website', ['Station'])

        # Adding model 'Picture'
        db.create_table('website_picture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scientificname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('family', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Family'])),
            ('subfamily', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Subfamily'], null=True, blank=True)),
            ('genus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Genus'])),
            ('species', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Species'])),
            ('subspecies', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Subspecies'], null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Country'], null=True, blank=True)),
            ('province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Province'], null=True, blank=True)),
            ('station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Station'], null=True, blank=True)),
            ('eventdate', self.gf('django.db.models.fields.DateField')()),
            ('view', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.ViewType'])),
            ('picture_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('website', ['Picture'])


    def backwards(self, orm):
        # Deleting model 'Family'
        db.delete_table('website_family')

        # Deleting model 'Subfamily'
        db.delete_table('website_subfamily')

        # Deleting model 'Genus'
        db.delete_table('website_genus')

        # Deleting model 'Species'
        db.delete_table('website_species')

        # Deleting model 'Subspecies'
        db.delete_table('website_subspecies')

        # Deleting model 'ViewType'
        db.delete_table('website_viewtype')

        # Deleting model 'Country'
        db.delete_table('website_country')

        # Deleting model 'Province'
        db.delete_table('website_province')

        # Deleting model 'Station'
        db.delete_table('website_station')

        # Deleting model 'Picture'
        db.delete_table('website_picture')


    models = {
        'website.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'website.family': {
            'Meta': {'object_name': 'Family'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'website.genus': {
            'Meta': {'object_name': 'Genus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'website.picture': {
            'Meta': {'object_name': 'Picture'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Country']", 'null': 'True', 'blank': 'True'}),
            'eventdate': ('django.db.models.fields.DateField', [], {}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Family']"}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'website.station': {
            'Meta': {'object_name': 'Station'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'website.subfamily': {
            'Meta': {'object_name': 'Subfamily'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'website.subspecies': {
            'Meta': {'object_name': 'Subspecies'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'website.viewtype': {
            'Meta': {'object_name': 'ViewType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['website']