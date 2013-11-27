# -*- coding: utf-8 -*-
import datetime
import os
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.conf import settings

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        os.system("cd %s && future_url --write" % settings.PROJECT_ROOT)

    def backwards(self, orm):
        "Write your backwards methods here."
        pass

    models = {
        'base.checklistitem': {
            'Meta': {'ordering': "('position',)", 'object_name': 'ChecklistItem'},
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'base.updatetracker': {
            'Meta': {'object_name': 'UpdateTracker'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_updating': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['base']
    symmetrical = True
