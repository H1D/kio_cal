# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Rubric'
        db.create_table('kio_cal_rubric', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('kio_cal', ['Rubric'])


    def backwards(self, orm):
        
        # Deleting model 'Rubric'
        db.delete_table('kio_cal_rubric')


    models = {
        'kio_cal.rubric': {
            'Meta': {'object_name': 'Rubric'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['kio_cal']
