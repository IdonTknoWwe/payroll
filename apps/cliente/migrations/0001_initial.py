# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2021-10-12 22:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClienteModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('commission', models.DecimalField(decimal_places=2, max_digits=9)),
                ('statusClient', models.SmallIntegerField(choices=[(1, 'ALTA'), (2, 'MEDIA'), (3, 'BAJA')])),
                ('rfcClient', models.CharField(max_length=13, unique=True)),
                ('primssAgreed', models.DecimalField(decimal_places=2, max_digits=15)),
                ('domicilie', models.CharField(blank=True, max_length=80)),
                ('legalRepresentative', models.CharField(blank=True, max_length=80)),
                ('numeroActa', models.CharField(blank=True, max_length=80)),
                ('dateConstitution', models.DateField()),
                ('noNotario', models.CharField(blank=True, max_length=80)),
                ('nameNotario', models.CharField(blank=True, max_length=80)),
                ('residenciaActa', models.CharField(blank=True, max_length=80)),
                ('noRppActa', models.CharField(blank=True, max_length=80)),
                ('numeroPoder', models.CharField(blank=True, max_length=80)),
                ('datePower', models.DateField()),
                ('noNotarioPoder', models.CharField(blank=True, max_length=80)),
                ('nameNotarioPoder', models.CharField(blank=True, max_length=80)),
                ('residenciaPoder', models.CharField(blank=True, max_length=80)),
                ('noRppPoder', models.CharField(blank=True, max_length=80)),
                ('isActive', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='archivos/')),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'REVISADA'), (1, 'DISPERSADA'), (2, 'PAGADA')])),
                ('cliente', models.CharField(max_length=13)),
                ('startPayroll', models.DateField()),
                ('endPayroll', models.DateField()),
                ('datePayroll', models.DateField()),
            ],
            options={
                'verbose_name': 'Archivo',
                'verbose_name_plural': 'Archivos',
            },
        ),
        migrations.CreateModel(
            name='PayeeIdModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'REVISADA'), (1, 'DISPERSADA'), (2, 'PAGADA')])),
                ('cliente', models.CharField(max_length=13)),
            ],
            options={
                'verbose_name': 'Nomina Cliente',
                'verbose_name_plural': 'Nomina Clientes',
            },
        ),
        migrations.CreateModel(
            name='PermitsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permiso', models.SmallIntegerField(choices=[(0, 'administrador'), (1, 'master'), (2, 'ejecutivo'), (3, 'tesoreria'), (4, 'facturacion'), (5, 'cliente')])),
                ('cliente', models.ManyToManyField(to='cliente.ClienteModel')),
            ],
            options={
                'verbose_name': 'Permiso',
                'verbose_name_plural': 'Permisos',
            },
        ),
    ]