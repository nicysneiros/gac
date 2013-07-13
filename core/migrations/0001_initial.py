# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Endereco'
        db.create_table('Endereco', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('logradouro', self.gf('django.db.models.fields.TextField')()),
            ('complemento', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('bairro', self.gf('django.db.models.fields.TextField')()),
            ('cidade', self.gf('django.db.models.fields.TextField')()),
            ('cep', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['Endereco'])

        # Adding model 'Cliente'
        db.create_table('Cliente', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('nome', self.gf('django.db.models.fields.TextField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('endereco', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Endereco'], db_column='ID_Endereco')),
            ('juridico', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'core', ['Cliente'])

        # Adding model 'Telefone'
        db.create_table('Telefone', (
            ('numero', self.gf('django.db.models.fields.TextField')(primary_key=True)),
        ))
        db.send_create_signal(u'core', ['Telefone'])

        # Adding M2M table for field clientes on 'Telefone'
        m2m_table_name = db.shorten_name('Telefone_clientes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('telefone', models.ForeignKey(orm[u'core.telefone'], null=False)),
            ('cliente', models.ForeignKey(orm[u'core.cliente'], null=False))
        ))
        db.create_unique(m2m_table_name, ['telefone_id', 'cliente_id'])

        # Adding model 'Servico'
        db.create_table('Servico', (
            ('id', self.gf('django.db.models.fields.TextField')(primary_key=True)),
            ('valor', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Cliente'], db_column='ID_Cliente')),
        ))
        db.send_create_signal(u'core', ['Servico'])

        # Adding model 'Produto'
        db.create_table('Produto', (
            (u'servico_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Servico'], unique=True, primary_key=True)),
            ('tamanho', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('categoria', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('foto', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Produto'])

        # Adding model 'Pedido'
        db.create_table('Pedido', (
            (u'servico_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Servico'], unique=True, primary_key=True)),
            ('descricao', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('prazo', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('desenho', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Pedido'])

        # Adding model 'Corporativo'
        db.create_table('Corporativo', (
            (u'pedido_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Pedido'], unique=True, primary_key=True)),
            ('qtd_P', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('qtd_M', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('qtd_G', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal(u'core', ['Corporativo'])

        # Adding model 'Personalizado'
        db.create_table('Personalizado', (
            (u'pedido_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Pedido'], unique=True, primary_key=True)),
            ('altura', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('largura', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'core', ['Personalizado'])

        # Adding model 'Despesa'
        db.create_table('Despesa', (
            ('id', self.gf('django.db.models.fields.TextField')(primary_key=True)),
            ('valor', self.gf('django.db.models.fields.FloatField')()),
            ('fornecedor', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('descricao', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('servico', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Servico'], db_column='ID_Servico')),
        ))
        db.send_create_signal(u'core', ['Despesa'])


    def backwards(self, orm):
        # Deleting model 'Endereco'
        db.delete_table('Endereco')

        # Deleting model 'Cliente'
        db.delete_table('Cliente')

        # Deleting model 'Telefone'
        db.delete_table('Telefone')

        # Removing M2M table for field clientes on 'Telefone'
        db.delete_table(db.shorten_name('Telefone_clientes'))

        # Deleting model 'Servico'
        db.delete_table('Servico')

        # Deleting model 'Produto'
        db.delete_table('Produto')

        # Deleting model 'Pedido'
        db.delete_table('Pedido')

        # Deleting model 'Corporativo'
        db.delete_table('Corporativo')

        # Deleting model 'Personalizado'
        db.delete_table('Personalizado')

        # Deleting model 'Despesa'
        db.delete_table('Despesa')


    models = {
        u'core.cliente': {
            'Meta': {'object_name': 'Cliente', 'db_table': "'Cliente'"},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'endereco': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Endereco']", 'db_column': "'ID_Endereco'"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'juridico': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nome': ('django.db.models.fields.TextField', [], {})
        },
        u'core.corporativo': {
            'Meta': {'object_name': 'Corporativo', 'db_table': "'Corporativo'", '_ormbases': [u'core.Pedido']},
            u'pedido_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Pedido']", 'unique': 'True', 'primary_key': 'True'}),
            'qtd_G': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'qtd_M': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'qtd_P': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        u'core.despesa': {
            'Meta': {'object_name': 'Despesa', 'db_table': "'Despesa'"},
            'descricao': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fornecedor': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'servico': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Servico']", 'db_column': "'ID_Servico'"}),
            'valor': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.endereco': {
            'Meta': {'object_name': 'Endereco', 'db_table': "'Endereco'"},
            'bairro': ('django.db.models.fields.TextField', [], {}),
            'cep': ('django.db.models.fields.TextField', [], {}),
            'cidade': ('django.db.models.fields.TextField', [], {}),
            'complemento': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logradouro': ('django.db.models.fields.TextField', [], {})
        },
        u'core.pedido': {
            'Meta': {'object_name': 'Pedido', 'db_table': "'Pedido'", '_ormbases': [u'core.Servico']},
            'descricao': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'desenho': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'prazo': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'servico_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Servico']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.personalizado': {
            'Meta': {'object_name': 'Personalizado', 'db_table': "'Personalizado'", '_ormbases': [u'core.Pedido']},
            'altura': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'largura': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'pedido_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Pedido']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.produto': {
            'Meta': {'object_name': 'Produto', 'db_table': "'Produto'", '_ormbases': [u'core.Servico']},
            'categoria': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'foto': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'servico_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Servico']", 'unique': 'True', 'primary_key': 'True'}),
            'tamanho': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'core.servico': {
            'Meta': {'object_name': 'Servico', 'db_table': "'Servico'"},
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Cliente']", 'db_column': "'ID_Cliente'"}),
            'id': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'valor': ('django.db.models.fields.FloatField', [], {'blank': 'True'})
        },
        u'core.telefone': {
            'Meta': {'object_name': 'Telefone', 'db_table': "'Telefone'"},
            'clientes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Cliente']", 'db_column': "'ID_Clientes'", 'symmetrical': 'False'}),
            'numero': ('django.db.models.fields.TextField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['core']