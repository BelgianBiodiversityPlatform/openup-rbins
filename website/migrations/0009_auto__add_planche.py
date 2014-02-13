# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Planche'
        db.create_table(u'website_planche', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('referenced_picture', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Picture'])),
            ('planche_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'website', ['Planche'])


    def backwards(self, orm):
        # Deleting model 'Planche'
        db.delete_table(u'website_planche')


    models = {
        u'website.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'website.family': {
            'Meta': {'ordering': "['name']", 'object_name': 'Family'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'website.genus': {
            'Meta': {'object_name': 'Genus'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Family']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'subfamily': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Subfamily']", 'null': 'True', 'blank': 'True'})
        },
        u'website.picture': {
            'Meta': {'object_name': 'Picture'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Country']", 'null': 'True', 'blank': 'True'}),
            'eventdate_verbatim': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Family']"}),
            'fileuri': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'genus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Genus']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origpathname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'picture_id': ('django.db.models.fields.IntegerField', [], {}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Province']", 'null': 'True', 'blank': 'True'}),
            'scientificname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Species']"}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Station']", 'null': 'True', 'blank': 'True'}),
            'subfamily': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Subfamily']", 'null': 'True', 'blank': 'True'}),
            'subspecies': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Subspecies']", 'null': 'True', 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.ViewType']"})
        },
        u'website.planche': {
            'Meta': {'object_name': 'Planche'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'planche_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'referenced_picture': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Picture']"})
        },
        u'website.province': {
            'Meta': {'object_name': 'Province'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'website.species': {
            'Meta': {'object_name': 'Species'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Family']", 'null': 'True', 'blank': 'True'}),
            'genus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Genus']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'subfamily': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Subfamily']", 'null': 'True', 'blank': 'True'})
        },
        u'website.station': {
            'Meta': {'object_name': 'Station'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'website.subfamily': {
            'Meta': {'object_name': 'Subfamily'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Family']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'website.subspecies': {
            'Meta': {'object_name': 'Subspecies'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Family']", 'null': 'True', 'blank': 'True'}),
            'genus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Genus']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Species']", 'null': 'True', 'blank': 'True'}),
            'subfamily': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Subfamily']", 'null': 'True', 'blank': 'True'})
        },
        u'website.viewtype': {
            'Meta': {'object_name': 'ViewType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['website']