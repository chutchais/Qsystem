# Generated by Django 3.0.5 on 2020-08-03 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('section', '0005_section_color'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['prefix']},
        ),
        migrations.AddIndex(
            model_name='section',
            index=models.Index(fields=['name'], name='idx_section_section_name'),
        ),
    ]
