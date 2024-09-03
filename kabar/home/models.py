import random

from django.db import models
from django.shortcuts import render

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from materials.models import MaterialPage, Category
from simple_pages.models import Banner, OtherLinks, Partners

from django.db.models import F


class HomePage(Page):
    # Для передачи дополнительного контекста в шаблон страницы (помимо определенных в модели полей)
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        main_materials = MaterialPage.get_main_materials(limit=5)
        important_materials = MaterialPage.get_important_materials(limit=2)
        # Последние материалы (для ленты)
        last_materials = MaterialPage.get_last_materials(limit=11)
        popular_materials = MaterialPage.get_top_news(lookback_days=360, limit=7)

        president_category = Category.objects.get(slug='president')
        president_materials = MaterialPage.get_materials_by_category(president_category, limit=7)
        first_president_material = president_materials.first()
        president_materials = president_materials[1:]

        parliament_category = Category.objects.get(slug='parliament')
        parliament_materials = MaterialPage.get_materials_by_category(parliament_category, limit=7)
        first_parliament_material = parliament_materials.first()
        parliament_materials = parliament_materials[1:]

        government_category = Category.objects.get(slug='government')
        government_materials = MaterialPage.get_materials_by_category(government_category, limit=7)
        first_government_material = government_materials.first()
        government_materials = government_materials[1:]

        regular_categories_materials = MaterialPage.get_regular_categories_materials(limit=10)

        business_category = Category.objects.get(slug='business')
        business_materials = MaterialPage.get_materials_by_category(business_category, limit=4)

        analytics_category = Category.objects.get(slug='analytics')
        analytics_materials = MaterialPage.get_materials_by_category(analytics_category, limit=2)

        press_center_category = Category.objects.get(slug='press-center')
        press_center_materials = MaterialPage.get_materials_by_category(press_center_category, limit=2)

        interview_category = Category.objects.get(slug='interview')
        interview_materials = MaterialPage.get_materials_by_category(interview_category, limit=3)

        photo_report_materials = MaterialPage.get_photo_report_materials(limit=2)
        video_report_materials = MaterialPage.get_video_report_materials(limit=3)

        region_materials = MaterialPage.get_region_materials(limit=9)

        tourism_category = Category.objects.get(slug='tourism')
        tourism_material = MaterialPage.get_last_material_by_category(tourism_category)

        personnel_category = Category.objects.get(slug='personnel')
        personnel_materials = MaterialPage.get_materials_by_category(personnel_category, limit=3)

        bishkek_events_category = Category.objects.get(slug='bishkek_events')
        bishkek_events_materials = MaterialPage.get_materials_by_category(bishkek_events_category, limit=4)

        banners = Banner.get_banners(pos='main')
        banner = random.choice(banners) if banners else None

        # # Если существует, будет инкрементировано поле views для выбранного баннера
        if banner:
            Banner.objects.filter(pk=banner.pk).update(views=F('views') + 1)

        other_links = OtherLinks.get_other_links()
        partners = Partners.get_partners()

        # Видео
        # last_video_materials = MaterialPage.get_last_video_materials(limit=5)
        # if last_video_materials.exists():
        #     last_video_material = last_video_materials[0]
        #     next_last_video_materials = last_video_materials[1:]
        # else:
        #     last_video_material = None
        #     next_last_video_materials = []

        context['main_materials'] = main_materials
        context['important_materials'] = important_materials
        context['last_materials'] = last_materials
        context['popular_materials'] = popular_materials
        context['first_president_material'] = first_president_material
        context['president_materials'] = president_materials
        context['first_parliament_material'] = first_parliament_material
        context['parliament_materials'] = parliament_materials
        context['first_government_material'] = first_government_material
        context['government_materials'] = government_materials
        context['regular_categories_materials'] = regular_categories_materials
        context['business_materials'] = business_materials
        context['banner'] = banner
        context['analytics_materials'] = analytics_materials
        context['press_center_materials'] = press_center_materials
        context['interview_materials'] = interview_materials
        context['photo_report_materials'] = photo_report_materials
        context['video_report_materials'] = video_report_materials
        context['region_materials'] = region_materials
        context['tourism_material'] = tourism_material
        context['other_links'] = other_links
        context['partners'] = partners
        context['personnel_materials'] = personnel_materials
        context['bishkek_events_materials'] = bishkek_events_materials

        # context['last_video_material'] = last_video_material
        # context['next_last_video_materials'] = next_last_video_materials

        return context

    class Meta:
        verbose_name = 'Главная'

