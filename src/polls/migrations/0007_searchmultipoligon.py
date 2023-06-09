# Generated by Django 2.2.12 on 2020-04-13 21:28

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_searchpoligon'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchMultiPoligon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('loc', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'verbose_name': 'Район поиска',
                'verbose_name_plural': 'Районы поиска',
            },
        ),
    ]
