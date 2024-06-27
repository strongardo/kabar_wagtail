import random

from django.db import models
from django.shortcuts import render

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from materials.models import MaterialPage
from simple_pages.models import Banner

from django.db.models import F


class HomePage(Page):
    # Для передачи дополнительного контекста в шаблон страницы (помимо определенных в модели полей)
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Главные материалы
        main_materials = MaterialPage.get_main_materials(limit=3)

        # Видео
        last_video_materials = MaterialPage.get_last_video_materials(limit=5)
        if last_video_materials.exists():
            last_video_material = last_video_materials[0]
            next_last_video_materials = last_video_materials[1:]
        else:
            last_video_material = None
            next_last_video_materials = []

        # Баннеры
        banners = Banner.get_banners()
        top_banners = [banner for banner in banners if banner.position == 'main_top']
        bottom_banners = [banner for banner in banners if banner.position == 'main_bottom']
        aside_banners = [banner for banner in banners if banner.position == 'aside']

        def choose_random_banner(banner_list):
            return random.choice(banner_list) if banner_list else None
        top_banner = choose_random_banner(top_banners)
        bottom_banner = choose_random_banner(bottom_banners)
        aside_banner = choose_random_banner(aside_banners)

        # Формирует список pk выбранных баннеров. pk попадет в список, если баннер существует
        selected_banners_pks = [banner.pk for banner in [top_banner, bottom_banner, aside_banner] if banner]
        # Если список pk не пуст, будет инкрементировано поле views для выбранных баннеров
        if selected_banners_pks:
            Banner.objects.filter(pk__in=selected_banners_pks).update(views=F('views') + 1)

        context['main_materials'] = main_materials
        context['last_video_material'] = last_video_material
        context['next_last_video_materials'] = next_last_video_materials
        context['top_banner'] = top_banner
        context['bottom_banner'] = bottom_banner
        context['aside_banner'] = aside_banner

        return context

    class Meta:
        verbose_name = 'Главная'

