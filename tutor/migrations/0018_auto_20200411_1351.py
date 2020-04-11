# Generated by Django 3.0.4 on 2020-04-11 17:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0017_job_session_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(help_text="Phone number must be entered in the format: '999-999-9999'. Up to 15 digits allowed.", max_length=17, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]