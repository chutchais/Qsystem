# Generated by Django 3.0.5 on 2021-01-21 06:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('section', '0007_auto_20200810_0915'),
        ('counter', '0006_auto_20200731_2324'),
        ('job', '0004_auto_20200803_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job_Archive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('queue_number', models.IntegerField(default=0)),
                ('on_process', models.BooleanField(default=False)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('started_date', models.DateTimeField(blank=True, null=True)),
                ('finished_date', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('counter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='jobs_archive', to='counter.Counter')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='jobs_archive', to='section.Section')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='jobs_archive', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_date'],
            },
        ),
        migrations.AddIndex(
            model_name='job_archive',
            index=models.Index(fields=['counter'], name='idx_job_archive_job_counter'),
        ),
        migrations.AddIndex(
            model_name='job_archive',
            index=models.Index(fields=['section'], name='idx_job_archive_job_section'),
        ),
        migrations.AddIndex(
            model_name='job_archive',
            index=models.Index(fields=['active'], name='idx_job_archive_job_active'),
        ),
    ]
