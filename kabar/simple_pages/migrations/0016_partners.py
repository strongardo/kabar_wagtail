# Generated by Django 5.0.3 on 2024-08-25 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_pages', '0015_otherlinks_is_active_alter_otherlinks_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('url', models.URLField(blank=True, null=True, verbose_name='Ссылка')),
                ('image', models.ImageField(blank=True, null=True, upload_to='other_links/', verbose_name='Изображение')),
                ('is_active', models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть партнера на сайте', verbose_name='Показать/Скрыть')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')),
            ],
            options={
                'verbose_name': 'Партнер',
                'verbose_name_plural': 'Партнеры',
            },
        ),
    ]
