# Generated by Django 2.2.12 on 2020-04-08 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_earthstation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decoder',
            name='station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='decoder', to='polls.EarthStation'),
        ),
        migrations.AlterField(
            model_name='encoder',
            name='station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.EarthStation'),
        ),
        migrations.AlterField(
            model_name='mks',
            name='stations',
            field=models.ManyToManyField(blank=True, to='polls.EarthStation', verbose_name='Наземный сегмент'),
        ),
        migrations.AlterField(
            model_name='redioline',
            name='station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.EarthStation'),
        ),
        migrations.AlterField(
            model_name='ssc',
            name='stations',
            field=models.ManyToManyField(blank=True, to='polls.EarthStation', verbose_name='Наземный сегмент'),
        ),
        migrations.DeleteModel(
            name='Station',
        ),
    ]