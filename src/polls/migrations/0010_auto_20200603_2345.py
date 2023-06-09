# Generated by Django 2.2.12 on 2020-06-03 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20200603_2334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='decoder',
            name='station',
        ),
        migrations.AddField(
            model_name='decoder',
            name='antenna',
            field=models.CharField(choices=[('AF', 'АФАР'), ('F', 'ФАР'), ('DISH', 'зеркало')], default='АФАР', max_length=128, verbose_name='Тип антенны'),
        ),
        migrations.AlterField(
            model_name='decoder',
            name='KPD',
            field=models.FloatField(default=1, verbose_name='Коэффициент полезного действия'),
        ),
        migrations.AlterField(
            model_name='decoder',
            name='sensity',
            field=models.FloatField(default=1, verbose_name='Уровень потерь антенны'),
        ),
        migrations.AlterField(
            model_name='decoder_antenna',
            name='type',
            field=models.CharField(choices=[('AF', 'АФАР'), ('F', 'ФАР'), ('DISH', 'зеркало')], default=80, max_length=128, verbose_name='Тип антенной системы'),
        ),
        migrations.AlterField(
            model_name='encoder_antenna',
            name='type',
            field=models.CharField(choices=[('AF', 'АФАР'), ('F', 'ФАР'), ('DISH', 'зеркало')], max_length=128, verbose_name='Тип антенной системы'),
        ),
    ]
