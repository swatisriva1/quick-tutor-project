# Generated by Django 3.0.5 on 2020-04-25 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0023_auto_20200422_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='acceptedjobs',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='requestedjobs',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
