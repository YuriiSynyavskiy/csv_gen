# Generated by Django 3.1.6 on 2021-02-17 11:38

import datetime
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csv_gen', '0005_auto_20210217_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='col_filter',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 2, 17, 11, 38, 32, 224090)),
        ),
    ]
