# Generated by Django 2.2.12 on 2020-06-05 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_auto_20200605_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='decoder',
            name='satellite',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='decoder', to='polls.Satellite'),
        ),
    ]
