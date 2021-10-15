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
            name='EnterpriseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('accountBancomer', models.CharField(blank=True, max_length=20)),
                ('clabeBancomer', models.CharField(blank=True, max_length=20)),
                ('accountSantander', models.CharField(blank=True, max_length=20)),
                ('clabeSantander', models.CharField(blank=True, max_length=20)),
                ('primss', models.DecimalField(decimal_places=2, max_digits=15)),
                ('rfc', models.CharField(max_length=13, unique=True)),
                ('legalRepresentative', models.CharField(blank=True, max_length=255)),
                ('recordNumber', models.CharField(blank=True, max_length=255)),
                ('dateConstitution', models.DateField()),
                ('noNotarioActa', models.CharField(blank=True, max_length=255)),
                ('nameNotarioActa', models.CharField(blank=True, max_length=255)),
                ('residenciaActa', models.CharField(blank=True, max_length=255)),
                ('noRppActa', models.CharField(blank=True, max_length=255)),
                ('numeroPoder', models.CharField(blank=True, max_length=255)),
                ('datePower', models.DateField()),
                ('noNotarioPoder', models.CharField(blank=True, max_length=255)),
                ('nameNotarioPoder', models.CharField(blank=True, max_length=255)),
                ('residenciaPoder', models.CharField(blank=True, max_length=255)),
                ('noRppPoder', models.CharField(blank=True, max_length=255)),
                ('isActive', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
    ]
