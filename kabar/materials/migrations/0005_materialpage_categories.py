# Generated by Django 5.0.1 on 2024-01-31 01:32

import modelcluster.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialpage',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='materials.category'),
        ),
    ]
