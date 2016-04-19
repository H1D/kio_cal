# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Release'
        db.create_table('kio_cal_release', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publication_ts', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_ready', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('kio_cal', ['Release'])

        # Adding M2M table for field column1 on 'Release'
        db.create_table('kio_cal_release_column1', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm['kio_cal.release'], null=False)),
            ('article', models.ForeignKey(orm['kio_cal.article'], null=False))
        ))
        db.create_unique('kio_cal_release_column1', ['release_id', 'article_id'])

        # Adding M2M table for field column2 on 'Release'
        db.create_table('kio_cal_release_column2', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm['kio_cal.release'], null=False)),
            ('article', models.ForeignKey(orm['kio_cal.article'], null=False))
        ))
        db.create_unique('kio_cal_release_column2', ['release_id', 'article_id'])

        # Adding M2M table for field column3 on 'Release'
        db.create_table('kio_cal_release_column3', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm['kio_cal.release'], null=False)),
            ('article', models.ForeignKey(orm['kio_cal.article'], null=False))
        ))
        db.create_unique('kio_cal_release_column3', ['release_id', 'article_id'])

        # Adding model 'Article'
        db.create_table('kio_cal_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rubric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kio_cal.Rubric'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('main_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('is_ready', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_dt', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modified_dt', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kio_cal', ['Article'])

        # Adding M2M table for field authors on 'Article'
        db.create_table('kio_cal_article_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['kio_cal.article'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('kio_cal_article_authors', ['article_id', 'user_id'])

        # Adding field 'Rubric.title'
        db.add_column('kio_cal_rubric', 'title', self.gf('django.db.models.fields.CharField')(default='?', max_length=256), keep_default=False)

        # Adding field 'Rubric.color'
        db.add_column('kio_cal_rubric', 'color', self.gf('colorfield.fields.ColorField')(default=' ', max_length=10), keep_default=False)

        # Adding M2M table for field authors on 'Rubric'
        db.create_table('kio_cal_rubric_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rubric', models.ForeignKey(orm['kio_cal.rubric'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('kio_cal_rubric_authors', ['rubric_id', 'user_id'])


    def backwards(self, orm):
        
        # Deleting model 'Release'
        db.delete_table('kio_cal_release')

        # Removing M2M table for field column1 on 'Release'
        db.delete_table('kio_cal_release_column1')

        # Removing M2M table for field column2 on 'Release'
        db.delete_table('kio_cal_release_column2')

        # Removing M2M table for field column3 on 'Release'
        db.delete_table('kio_cal_release_column3')

        # Deleting model 'Article'
        db.delete_table('kio_cal_article')

        # Removing M2M table for field authors on 'Article'
        db.delete_table('kio_cal_article_authors')

        # Deleting field 'Rubric.title'
        db.delete_column('kio_cal_rubric', 'title')

        # Deleting field 'Rubric.color'
        db.delete_column('kio_cal_rubric', 'color')

        # Removing M2M table for field authors on 'Rubric'
        db.delete_table('kio_cal_rubric_authors')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'kio_cal.article': {
            'Meta': {'ordering': "('created_dt',)", 'object_name': 'Article'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_dt': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ready': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'main_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified_dt': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'rubric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kio_cal.Rubric']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'kio_cal.release': {
            'Meta': {'ordering': "('publication_ts',)", 'object_name': 'Release'},
            'column1': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'release_col_1'", 'symmetrical': 'False', 'to': "orm['kio_cal.Article']"}),
            'column2': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'release_col_2'", 'symmetrical': 'False', 'to': "orm['kio_cal.Article']"}),
            'column3': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'release_col_3'", 'symmetrical': 'False', 'to': "orm['kio_cal.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ready': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publication_ts': ('django.db.models.fields.DateTimeField', [], {})
        },
        'kio_cal.rubric': {
            'Meta': {'object_name': 'Rubric'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'color': ('colorfield.fields.ColorField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['kio_cal']
