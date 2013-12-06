# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'medialibrary_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['medialibrary.Category'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
        ))
        db.send_create_signal(u'medialibrary', ['Category'])

        # Adding model 'MediaFile'
        db.create_table(u'medialibrary_mediafile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('copyright', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('file_size', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'medialibrary', ['MediaFile'])

        # Adding M2M table for field categories on 'MediaFile'
        m2m_table_name = db.shorten_name(u'medialibrary_mediafile_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mediafile', models.ForeignKey(orm[u'medialibrary.mediafile'], null=False)),
            ('category', models.ForeignKey(orm[u'medialibrary.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['mediafile_id', 'category_id'])

        # Adding model 'MediaFileTranslation'
        db.create_table(u'medialibrary_mediafiletranslation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', to=orm['medialibrary.MediaFile'])),
            ('language_code', self.gf('django.db.models.fields.CharField')(default='de', max_length=10)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'medialibrary', ['MediaFileTranslation'])

        # Adding unique constraint on 'MediaFileTranslation', fields ['parent', 'language_code']
        db.create_unique(u'medialibrary_mediafiletranslation', ['parent_id', 'language_code'])


    def backwards(self, orm):
        # Removing unique constraint on 'MediaFileTranslation', fields ['parent', 'language_code']
        db.delete_unique(u'medialibrary_mediafiletranslation', ['parent_id', 'language_code'])

        # Deleting model 'Category'
        db.delete_table(u'medialibrary_category')

        # Deleting model 'MediaFile'
        db.delete_table(u'medialibrary_mediafile')

        # Removing M2M table for field categories on 'MediaFile'
        db.delete_table(db.shorten_name(u'medialibrary_mediafile_categories'))

        # Deleting model 'MediaFileTranslation'
        db.delete_table(u'medialibrary_mediafiletranslation')


    models = {
        u'medialibrary.category': {
            'Meta': {'ordering': "['parent__title', 'title']", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['medialibrary.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'medialibrary.mediafile': {
            'Meta': {'ordering': "['-created']", 'object_name': 'MediaFile'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['medialibrary.Category']", 'null': 'True', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        u'medialibrary.mediafiletranslation': {
            'Meta': {'unique_together': "(('parent', 'language_code'),)", 'object_name': 'MediaFileTranslation'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'default': "'de'", 'max_length': '10'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': u"orm['medialibrary.MediaFile']"})
        }
    }

    complete_apps = ['medialibrary']