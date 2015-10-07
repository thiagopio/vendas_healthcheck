# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table(u'healthcheck_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('environment', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'healthcheck', ['Project'])

        # Adding M2M table for field related_project on 'Project'
        m2m_table_name = db.shorten_name(u'healthcheck_project_related_project')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_project', models.ForeignKey(orm[u'healthcheck.project'], null=False)),
            ('to_project', models.ForeignKey(orm[u'healthcheck.project'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_project_id', 'to_project_id'])

        # Adding model 'StatusResponse'
        db.create_table(u'healthcheck_statusresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthcheck.Project'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=100)),
            ('response_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('status', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'healthcheck', ['StatusResponse'])


    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table(u'healthcheck_project')

        # Removing M2M table for field related_project on 'Project'
        db.delete_table(db.shorten_name(u'healthcheck_project_related_project'))

        # Deleting model 'StatusResponse'
        db.delete_table(u'healthcheck_statusresponse')


    models = {
        u'healthcheck.project': {
            'Meta': {'object_name': 'Project'},
            'environment': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'related_project': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['healthcheck.Project']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'healthcheck.statusresponse': {
            'Meta': {'object_name': 'StatusResponse'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['healthcheck.Project']"}),
            'response_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['healthcheck']