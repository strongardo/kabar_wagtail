# Generated by Django 5.0.3 on 2024-08-23 17:02

import django.db.models.deletion
import wagtail.contrib.routable_page.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0034_alter_regioncategory_options_materialpage_region'),
        ('wagtailcore', '0091_remove_revision_submitted_for_moderation'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegionCategoryPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'verbose_name': 'Страница регионов',
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.AlterField(
            model_name='materialpage',
            name='region',
            field=models.ForeignKey(blank=True, help_text='Выберите, только если материал относится к определенному региону', null=True, on_delete=django.db.models.deletion.SET_NULL, to='materials.regioncategory', verbose_name='Регион'),
        ),
    ]
