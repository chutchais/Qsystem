# Generated by Django 2.1.5 on 2019-07-13 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('section', '0003_auto_20190713_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='prefix',
            field=models.CharField(blank=True, max_length=1),
        ),
    ]
