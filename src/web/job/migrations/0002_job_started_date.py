# Generated by Django 2.1.5 on 2019-07-14 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='started_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]