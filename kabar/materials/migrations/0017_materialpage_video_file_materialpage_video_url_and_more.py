# Generated by Django 5.0.1 on 2024-03-13 04:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0016_materialpage_is_main'),
        ('wagtaildocs', '0012_uploadeddocument'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialpage',
            name='video_file',
            field=models.ForeignKey(blank=True, help_text='Или загрузите файл видео', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.document'),
        ),
        migrations.AddField(
            model_name='materialpage',
            name='video_url',
            field=models.URLField(blank=True, help_text='Добавьте ссылку на видео с YouTube или другой платформы', null=True, verbose_name='Ссылка на видео'),
        ),
        migrations.AlterField(
            model_name='materialpage',
            name='is_main',
            field=models.BooleanField(default=False, help_text='Если выбрать, материал будет отображаться в разделе главных новостей, вверху главной страницы', verbose_name='Главная новость'),
        ),
    ]
