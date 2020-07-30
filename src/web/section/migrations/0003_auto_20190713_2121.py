# Generated by Django 2.1.5 on 2019-07-13 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('section', '0002_remove_section_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='maximum_number',
            field=models.IntegerField(default=200),
        ),
        migrations.AddField(
            model_name='section',
            name='starting_number',
            field=models.IntegerField(default=0),
        ),
    ]
