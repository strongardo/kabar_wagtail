# Generated by Django 5.0.3 on 2024-08-28 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0036_alter_author_bio_alter_author_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='slug',
            field=models.SlugField(blank=True, max_length=80, null=True, unique=True),
        ),
    ]
