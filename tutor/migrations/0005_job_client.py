# Generated by Django 3.0.2 on 2020-03-21 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0004_remove_job_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tutor.Profile'),
        ),
    ]
