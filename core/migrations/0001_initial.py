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
            ('Logradouro', self.gf('django.db.models.fields.TextField')()),
            ('Complemento', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('Bairro', self.gf('django.db.models.fields.TextField')()),
            ('Cidade', self.gf('django.db.models.fields.TextField')()),
            ('CEP', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'atelier', ['Endereco'])

        # Adding model 'Cliente'
        db.create_table('Cliente', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('Nome', self.gf('django.db.models.fields.TextField')()),
            ('Email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('Endereco', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atelier.Endereco'], db_column='ID_Endereco')),
            ('Foto', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'atelier', ['Cliente'])

        # Adding model 'Pessoa_Fisica'
        db.create_table('Pessoa_Fisica', (
            (u'cliente_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atelier.Cliente'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'atelier', ['Pessoa_Fisica'])

        # Adding model 'Pessoa_Juridica'
        db.create_table('Pessoa_Juridica', (
            (u'cliente_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atelier.Cliente'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'atelier', ['Pessoa_Juridica'])

        # Adding model 'Telefone'
        db.create_table('Telefone', (
            ('Numero', self.gf('django.db.models.fields.TextField')(primary_key=True)),
        ))
        db.send_create_signal(u'atelier', ['Telefone'])

        # Adding M2M table for field Clientes on 'Telefone'
        m2m_table_name = db.shorten_name('Telefone_Clientes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('telefone', models.ForeignKey(orm[u'atelier.telefone'], null=False)),
            ('cliente', models.ForeignKey(orm[u'atelier.cliente'], null=False))
        ))
        db.create_unique(m2m_table_name, ['telefone_id', 'cliente_id'])

        # Adding model 'Servico'
        db.create_table('Servico', (
            ('id', self.gf('django.db.models.fields.TextField')(primary_key=True)),
            ('Valor', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('Cliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atelier.Cliente'], db_column='ID_Cliente')),
        ))
        db.send_create_signal(u'atelier', ['Servico'])

        # Adding model 'Produto'
        db.create_table('Produto', (
            (u'servico_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atelier.Servico'], unique=True, primary_key=True)),
            ('Tamanho', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('Categoria', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('Foto', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'atelier', ['Produto'])

        # Adding model 'Pedido'
        db.create_table('Pedido', (
            (u'servico_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atelier.Servico'], unique=True, primary_key=True)),
            ('Descricao', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('Prazo', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('Desenho', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'atelier', ['Pedido'])

        # Adding model 'Corporativo'
        db.create_table('Corporativo', (
            (u'pedido_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atelier.Pedido'], unique=True, primary_key=True)),
            ('Qtd_P', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('Qtd_M', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('Qtd_G', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal(u'atelier', ['Corporativo'])

        # Adding model 'Personalizado'
        db.create_table('Personalizado', (
            (u'pedido_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atelier.Pedido'], unique=True, primary_key=True)),
            ('Altura', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('Largura', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'atelier', ['Personalizado'])

        # Adding model 'Despesa'
        db.create_table('Despesa', (
            ('id', self.gf('django.db.models.fields.TextField')(primary_key=True)),
            ('Valor', self.gf('django.db.models.fields.FloatField')()),
            ('Fornecedor', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('Descricao', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('Servico', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atelier.Servico'], db_column='ID_Servico')),
        ))
        db.send_create_signal(u'atelier', ['Despesa'])


    def backwards(self, orm):
        # Deleting model 'Endereco'
        db.delete_table('Endereco')

        # Deleting model 'Cliente'
        db.delete_table('Cliente')

        # Deleting model 'Pessoa_Fisica'
        db.delete_table('Pessoa_Fisica')

        # Deleting model 'Pessoa_Juridica'
        db.delete_table('Pessoa_Juridica')

        # Deleting model 'Telefone'
        db.delete_table('Telefone')

        # Removing M2M table for field Clientes on 'Telefone'
        db.delete_table(db.shorten_name('Telefone_Clientes'))

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
        u'atelier.cliente': {
            'Email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'Endereco': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atelier.Endereco']", 'db_column': "'ID_Endereco'"}),
            'Foto': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'Meta': {'object_name': 'Cliente', 'db_table': "'Cliente'"},
            'Nome': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        u'atelier.corporativo': {
            'Meta': {'object_name': 'Corporativo', 'db_table': "'Corporativo'", '_ormbases': [u'atelier.Pedido']},
            'Qtd_G': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'Qtd_M': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'Qtd_P': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            u'pedido_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atelier.Pedido']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'atelier.despesa': {
            'Descricao': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'Fornecedor': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'Meta': {'object_name': 'Despesa', 'db_table': "'Despesa'"},
            'Servico': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atelier.Servico']", 'db_column': "'ID_Servico'"}),
            'Valor': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.TextField', [], {'primary_key': 'True'})
        },
        u'atelier.endereco': {
            'Bairro': ('django.db.models.fields.TextField', [], {}),
            'CEP': ('django.db.models.fields.TextField', [], {}),
            'Cidade': ('django.db.models.fields.TextField', [], {}),
            'Complemento': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'Logradouro': ('django.db.models.fields.TextField', [], {}),
            'Meta': {'object_name': 'Endereco', 'db_table': "'Endereco'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'atelier.pedido': {
            'Descricao': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'Desenho': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Pedido', 'db_table': "'Pedido'", '_ormbases': [u'atelier.Servico']},
            'Prazo': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'servico_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atelier.Servico']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'atelier.personalizado': {
            'Altura': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'Largura': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'Meta': {'object_name': 'Personalizado', 'db_table': "'Personalizado'", '_ormbases': [u'atelier.Pedido']},
            u'pedido_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atelier.Pedido']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'atelier.pessoa_fisica': {
            'Meta': {'object_name': 'Pessoa_Fisica', 'db_table': "'Pessoa_Fisica'", '_ormbases': [u'atelier.Cliente']},
            u'cliente_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atelier.Cliente']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'atelier.pessoa_juridica': {
            'Meta': {'object_name': 'Pessoa_Juridica', 'db_table': "'Pessoa_Juridica'", '_ormbases': [u'atelier.Cliente']},
            u'cliente_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atelier.Cliente']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'atelier.produto': {
            'Categoria': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'Foto': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Produto', 'db_table': "'Produto'", '_ormbases': [u'atelier.Servico']},
            'Tamanho': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'servico_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atelier.Servico']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'atelier.servico': {
            'Cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atelier.Cliente']", 'db_column': "'ID_Cliente'"}),
            'Meta': {'object_name': 'Servico', 'db_table': "'Servico'"},
            'Valor': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.TextField', [], {'primary_key': 'True'})
        },
        u'atelier.telefone': {
            'Clientes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['atelier.Cliente']", 'db_column': "'ID_Clientes'", 'symmetrical': 'False'}),
            'Meta': {'object_name': 'Telefone', 'db_table': "'Telefone'"},
            'Numero': ('django.db.models.fields.TextField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['atelier']