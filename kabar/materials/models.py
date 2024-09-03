import random
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Count, Q
from django import forms
from django.utils import timezone
from django.http import HttpResponseRedirect
from datetime import timedelta, datetime
from wagtail.models import Page, Orderable
from wagtail.documents.models import Document
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.snippets.models import register_snippet
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from .utils import get_paginated_page
from .forms import DateFilterForm
from simple_pages.models import Banner
from django.db.models import F


# ХРАНИЛИЩЕ ДЛЯ ТЕГОВ
# По сути это не сами теги, а хранилище для них, связанное с определенной страницей
class MaterialPageTag(TaggedItemBase):
    # Поле ParentalKey используется для создания связей "родитель-потомок" между моделями.
    content_object = ParentalKey(
        'MaterialPage',  # хранилище используется для страниц 'MaterialPage'

        on_delete=models.CASCADE,  # определяет, что произойдет со связанным объектом
        # (в данном случае, с тегом), когда объект, с которым он связан
        # (в данном случае, экземпляр MaterialPage), будет удален.
        # Здесь установлено значение CASCADE, что означает, что при удалении MaterialPage,
        # все связанные с ним теги также будут удалены.

        related_name='tagged_items',  # Явное имя для обращения к тегам из шаблона (не обязательно)
    )


class FilterableMaterialsIndexPage(RoutablePageMixin, Page):
    # Этот маршрут соответствует базовому URL страницы (/archive/), и активируется при его посещении.
    @route(r'^$')
    def submit_filter_form(self, request):
        # Создает экземпляр формы, используя данные из GET-запроса, или None, если GET-запрос пуст.
        form = DateFilterForm(request.GET or None)
        if form.is_valid():
            # Извлекает дату из данных формы.
            date = form.cleaned_data['date']
            # Формирует URL для редиректа, добавляя к базовому URL страницы строковое представление даты.
            # В итоге получается URL такого формата: /archive/2024-03-01/
            url = self.url + date.strftime('%Y-%m-%d') + '/'
            # Выполняет редирект на сформированный URL.
            return HttpResponseRedirect(url)

        # Если форма не была отправлена или содержит некорректные данные, снова отображает страницу с формой.
        return self.render(request, context_overrides={
            'form': form,
        })

    # Этот маршрут соответствует URL с датой (например, /archive/2024-03-01/)
    @route(r'^(?P<date_str>\d{4}-\d{2}-\d{2})/$')
    @route(r'^(?P<date_str>\d{4}-\d{2}-\d{2})/page_(?P<page_number>\d+)/$')
    def filter_by_date(self, request, date_str, page_number=1):
        try:
            # Преобразует строку даты из URL в объект datetime
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            # В случае ошибки преобразования даты возвращает страницу с ошибкой 404.
            raise Http404("Некорректный формат даты")

        # Создает экземпляр формы с начальным значением даты, соответствующим полученной из URL.
        form = DateFilterForm(initial={'date': date_str})
        materials = MaterialPage.get_materials_by_date(date)
        page_obj = get_paginated_page(materials, page_number, per_page=3)

        return self.render(request, context_overrides={
            'form': form,
            'page_obj': page_obj,
            'date_str': date_str,  # для формирования routablepageurl в пагинации
        })

    parent_page_types = ['home.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = 'Страница отфильтрованных материалов'


# СТРАНИЦА ВСЕХ МАТЕРИАЛОВ
# RoutablePageMixin предоставляет удобный способ обработки запросов для разных под-URL с
# использованием декораторов, позволяя странице реагировать на разные маршруты и возвращать соответствующие
# представления. Важен порядок наследования - сначала RoutablePageMixin, затем Page!!!
class MaterialsIndexPage(RoutablePageMixin, Page):
    @route(r'^$')
    @route(r'^page_(?P<page_number>\d+)/$')
    def all_materials(self, request, page_number=1):
        materials = MaterialPage.get_materials()

        page_obj = get_paginated_page(materials, page_number, per_page=10)
        # get_paginated_page импортируется из модуля utils и возвращает отдельную страницу пагинатора с материалами
        # для этой страницы

        # Возвращает результат работы метода render, передавая в контекст шаблона дополнительную информацию
        return self.render(request, context_overrides={
            'page_obj': page_obj,
        })

    # Parent page / subpage type rules
    parent_page_types = ['home.HomePage']
    subpage_types = ['MaterialPage']

    class Meta:
        verbose_name = 'Страница материалов'


class CategoryPage(RoutablePageMixin, Page):
    @route(r'^(?P<category_slug>[-\w]+)/$')
    @route(r'^(?P<category_slug>[-\w]+)/page_(?P<page_number>\d+)/$')
    def materials_by_category(self, request, category_slug, page_number=1):
        try:
            # noinspection PyUnresolvedReferences
            current_category = Category.objects.get(slug=category_slug)
            materials = MaterialPage.get_materials_by_category(current_category)
            page_obj = get_paginated_page(materials, page_number, per_page=10)

            return self.render(request, context_overrides={
                'current_category': current_category,
                'page_obj': page_obj,
                'custom_title': current_category.name,
                'custom_description': f"Новости категории «{current_category.name}»"
            })
        except ObjectDoesNotExist:
            # Если категория не найдена, можно вернуть пользователю страницу 404
            raise Http404("Категория не найдена")

    @route(r'^$')  # Маршрут для корневого URL
    def base_category_route(self, request, *args, **kwargs):
        raise Http404("Страница не найдена")

    parent_page_types = ['home.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = 'Страница категорий'


class RegionCategoryPage(RoutablePageMixin, Page):
    @route(r'^(?P<category_slug>[-\w]+)/$')
    @route(r'^(?P<category_slug>[-\w]+)/page_(?P<page_number>\d+)/$')
    def materials_by_region(self, request, category_slug, page_number=1):
        try:
            # noinspection PyUnresolvedReferences
            current_region_category = RegionCategory.objects.get(slug=category_slug)
            materials = MaterialPage.get_materials_by_region(current_region_category)
            page_obj = get_paginated_page(materials, page_number, per_page=3)

            return self.render(request, context_overrides={
                'page_obj': page_obj,
                'custom_title': current_region_category.name,
                'custom_description': f"Новости региона «{current_region_category.name}»"
            })
        except ObjectDoesNotExist:
            # Если категория не найдена, можно вернуть пользователю страницу 404
            raise Http404("Регион не найден")

    @route(r'^$')  # Маршрут для корневого URL
    def base_category_route(self, request, *args, **kwargs):
        raise Http404("Страница не найдена")

    parent_page_types = ['home.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = 'Страница регионов'


class AuthorPage(RoutablePageMixin, Page):
    @route(r'^(?P<author_slug>[-\w]+)/$')
    @route(r'^(?P<author_slug>[-\w]+)/page_(?P<page_number>\d+)/$')
    def materials_by_author(self, request, author_slug, page_number=1):
        try:
            current_author = Author.objects.get(slug=author_slug)
            materials = MaterialPage.get_materials_by_author(author=current_author)
            page_obj = get_paginated_page(materials, page_number, per_page=7)

            banners = list(Banner.get_banners(pos='aside'))
            selected_banners = random.sample(banners, min(len(banners), 2))
            first_banner = selected_banners[0] if len(selected_banners) > 0 else None
            second_banner = selected_banners[1] if len(selected_banners) > 1 else None
            if first_banner:
                Banner.objects.filter(pk=first_banner.pk).update(views=F('views') + 1)
            if second_banner:
                Banner.objects.filter(pk=second_banner.pk).update(views=F('views') + 1)

            return self.render(request, context_overrides={
                'current_author': current_author,
                'page_obj': page_obj,
                'total_materials': page_obj.paginator.count,
                'custom_title': f"Новости от {current_author.name}",
                'custom_description': f"Новости, написанные {current_author.name}",
                'first_banner': first_banner,
                'second_banner': second_banner,
            })
        except ObjectDoesNotExist:
            raise Http404("Автор не найден")

    @route(r'^$')  # Маршрут для корневого URL
    def base_author_route(self, request, *args, **kwargs):
        raise Http404("Страница не найдена")

    parent_page_types = ['home.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = 'Страница авторов'


class MaterialPage(Page):
    pub_date = models.DateTimeField("Дата и время публикации", default=timezone.now)
    body = RichTextField(verbose_name='Контент', blank=True)
    view_count = models.PositiveIntegerField(default=0)

    # Поле ParentalManyToManyField предоставляет связь "родитель-потомок" для многие ко многим.
    # Каждый экземпляр модели MaterialPage может иметь несколько авторов,
    # и каждый автор может быть связан с несколькими страницами.
    # authors = ParentalManyToManyField('materials.Author', verbose_name='Авторы', blank=True)
    author = models.ForeignKey(
        'materials.Author', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автор'
    )

    category = models.ForeignKey(
        'materials.Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория'
    )

    region = models.ForeignKey(
        'materials.RegionCategory', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Регион',
        help_text="Выберите, только если материал относится к определенному региону"
    )

    # categories = ParentalManyToManyField('materials.Category', verbose_name='Категории', blank=True)

    # ClusterTaggableManager - поле для добавления и управления тегами страницы.
    # Даёт возможность указать с каким хранилищем тегов(TaggedItemBase) связаны теги этой страницы
    # По сути дает возможность странице иметь теги
    tags = ClusterTaggableManager(through=MaterialPageTag, blank=True)

    main_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name="Основное изображение",
    )

    video_url = models.URLField("Ссылка на видео с YouTube", blank=True, null=True,
                                help_text="Добавьте ссылку на видео с YouTube или Vimeo")

    fb_video_url = models.URLField("Ссылка на видео c Facebook", blank=True, null=True,
                                   help_text="Добавьте ссылку на видео с Facebook")

    video_file = models.ForeignKey(
        Document, null=True, blank=True, on_delete=models.SET_NULL, related_name="+",
        verbose_name="Видео-файл",
        help_text="Загрузите видео-файл"
    )

    is_main = models.BooleanField(default=False, verbose_name="Главная новость",
                                  help_text="Если выбрать, материал будет отображаться в разделе главных новостей, "
                                            "вверху главной страницы")

    is_important = models.BooleanField(default=False, verbose_name="Важная новость",
                                       help_text="Если выбрать, материал будет отображаться в разделе важных новостей, "
                                                 "вверху главной страницы рядом с главными")

    is_announcement = models.BooleanField(default=False, verbose_name="Анонс",
                                          help_text="Выберите, если материал является анонсом")

    is_live = models.BooleanField(default=False, verbose_name="Live",
                                  help_text="Выберите, если материал посвящен текущей пресс-конференции")

    is_survey = models.BooleanField(default=False, verbose_name="Опрос",
                                    help_text="Выберите, если материал содержит опрос")

    is_photo_report = models.BooleanField(default=False, verbose_name="Фоторепортаж",
                                          help_text="Выберите, если материал содержит фоторепортаж. Этот материал "
                                                    "попадет в секцию с фоторепортажами")

    is_video_report = models.BooleanField(default=False, verbose_name="Видеорепортаж",
                                          help_text="Выберите, если материал содержит видеорепортаж. Этот материал "
                                                    "попадет в секцию с видеорепортажами")

    # SearchField определяет, по каким полям модели будет производиться поиск(обычный поиск на сайте).
    # Некоторые стандартные поля(title, slug, search_description) + 'body'
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('pub_date'),
            FieldPanel('author', widget=forms.Select),
            FieldPanel('category', widget=forms.Select),
            FieldPanel('region', widget=forms.Select),
        ], heading="Информация о материале"),
        FieldPanel('body'),

        # InlinePanel - позволяет встраивать другие модели (обычно Orderable) в админку страницы
        # Также автоматически создает виртуальное поле gallery_images в текущей модели
        InlinePanel('gallery_images', label="Изображение"),
        # FieldPanel('main_image'),

        MultiFieldPanel([
            FieldPanel('video_url'),
            FieldPanel('fb_video_url'),
            FieldPanel('video_file'),
        ], heading="Видео"),

        MultiFieldPanel([
            FieldPanel('is_main'),
            FieldPanel('is_important'),
            FieldPanel('is_announcement'),
            FieldPanel('is_live'),
            FieldPanel('is_survey'),
            FieldPanel('is_photo_report'),
            FieldPanel('is_video_report'),
        ], heading="Отметки"),

        FieldPanel('tags'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        current_category = self.category

        # Проверяем, что у материала есть категория
        if current_category:
            # Вызываем get_similar_materials для текущей категории и идентификатора страницы
            similar_materials = MaterialPage.get_similar_materials(category=current_category, current_page_pk=self.pk,
                                                                   limit=3)
        else:
            similar_materials = MaterialPage.objects.none()  # Возвращаем пустой запрос, если категория не задана

        # print(f'+++++++++++++++++++{similar_materials}+++++++++++++++++++++')

        top_news = MaterialPage.get_top_news(limit=6)

        banners = Banner.get_banners(pos='aside')
        banner = random.choice(banners) if banners else None

        if banner:
            Banner.objects.filter(pk=banner.pk).update(views=F('views') + 1)

        business_category = Category.objects.get(slug='business')
        business_materials = MaterialPage.get_materials_by_category_with_author(business_category, limit=3)

        # prev_material, next_material = MaterialPage.get_adjacent_materials(self)

        author_page = AuthorPage.objects.live().first()

        context['top_news'] = top_news
        context['similar_materials'] = similar_materials
        context['banner'] = banner
        context['business_materials'] = business_materials
        context['business_materials'] = business_materials
        context['author_page'] = author_page

        return context

    # Переопределяется стандартный метод save() для определения основного изображения при сохранении материала
    def save(self, *args, **kwargs):
        # Попытка получить первое изображение из галереи
        first_gallery_image = self.gallery_images.first()

        if first_gallery_image:
            # Если галерея не пуста и main_image нуждается в обновлении
            if not self.main_image or self.main_image != first_gallery_image.image:
                self.main_image = first_gallery_image.image
        else:
            # Если галерея пуста, устанавливаем main_image в None
            self.main_image = None

        super(MaterialPage, self).save(*args, **kwargs)

    @classmethod
    def get_materials(cls):
        return (
            cls.objects.live()
            .only('title', 'pub_date', 'view_count', 'category', 'main_image')
            .select_related('category')
            .select_related('main_image')
            .order_by('-first_published_at')
        )

        # Использование only() уменьшает количество данных, передаваемых между базой данных и приложением,
        # поскольку извлекаются только указанные поля.
        # Это особенно полезно, когда модели содержат поля с большим объемом данных,
        # такие как текстовые поля TextField или поля с изображениями ImageField, которые не всегда нужны.
        # .prefetch_related() - загружает все связанные данные для набора материалов одним запросом.
        # Затем, когда вы итерируете по материалам и обращаетесь к их категориям в шаблоне,
        # Django не выполняет дополнительные запросы к базе данных для каждого материала.
        # Вместо этого он использует уже загруженные данные, что значительно уменьшает общую нагрузку на базу данных.
        # select_related используется для оптимизации запросов к базе данных
        # и наиболее эффективен для одиночных связей (ForeignKey или OneToOneField)
        # prefetch_related подходит связей многие-ко-многим (ManyToManyField),
        # где необходимо извлечь множество связанных объектов.

    @classmethod
    def get_last_materials(cls, limit=11):
        return (
            cls.objects.live()
            .only('title', 'pub_date', 'view_count', 'author')
            .select_related('author')
            .order_by('-first_published_at')[:limit]
        )

    @classmethod
    def get_regular_categories_materials(cls, limit=12):
        return (
            cls.objects.live()
            .filter(category__is_basic=False)
            # .exclude(category__slug__in=['business', 'analytics', 'press_center', 'events'])
            # Исключаем указанные категории
            .only('title', 'pub_date', 'view_count', 'main_image', 'category')
            .select_related('main_image')
            .select_related('category')
            .order_by('-first_published_at')[:limit]
        )

    @classmethod
    def get_region_materials(cls, limit=12):
        return (
            cls.objects.live()
            .filter(region__isnull=False)  # Фильтр для материалов, у которых поле region не пустое
            .only('title', 'pub_date', 'view_count', 'main_image', 'category')
            .select_related('main_image')
            .select_related('category')
            .order_by('-first_published_at')[:limit]
        )

    @classmethod
    def get_materials_by_category(cls, category, limit=None):
        query = (
            cls.objects.live()
            .filter(category=category)
            .only('title', 'pub_date', 'view_count', 'category', 'main_image')
            .select_related('category')
            .select_related('main_image')
            .order_by('-first_published_at')
        )

        if limit is not None:
            return query[:limit]

        return query

    @classmethod
    def get_materials_by_category_with_author(cls, category, limit=3):
        return (
            cls.objects.live()
            .filter(category=category)
            .only('title', 'pub_date', 'view_count', 'author', 'main_image')
            .select_related('author')
            .select_related('main_image')
            .order_by('-first_published_at')[:limit]
        )

    @classmethod
    def get_last_material_by_category(cls, category):
        return (
            cls.objects.live()
            .filter(category=category)
            .only('title', 'pub_date', 'view_count', 'category', 'main_image')
            .select_related('category')
            .select_related('main_image')
            .order_by('-first_published_at')
            .first()
        )

    @classmethod
    def get_materials_by_region(cls, region, limit=None):
        query = (
            cls.objects.live()
            .filter(region=region)
            .only('title', 'pub_date', 'view_count', 'category', 'main_image')
            .select_related('category')
            .select_related('main_image')
            .order_by('-first_published_at')
        )

        if limit is not None:
            return query[:limit]

        return query

    @classmethod
    def get_materials_by_author(cls, author):
        return (
            cls.objects.live()
            .filter(author=author)
            .only('title', 'pub_date', 'main_image')
            .select_related('main_image')
            .order_by('-first_published_at')
        )

    @classmethod
    def get_materials_by_date(cls, date):
        return (
            cls.objects.live()
            .filter(pub_date__date=date)
            .only('title', 'pub_date', 'view_count', 'category', 'main_image')
            .select_related('category')
            .select_related('main_image')
            .order_by('-first_published_at')
        )

    @classmethod
    def get_similar_materials(cls, category, current_page_pk, limit=4, lookback_days=100):
        now = timezone.now()
        start_date = now - timedelta(days=lookback_days)

        # Вычисляем разницу в днях и выбираем случайное число дней в этом диапазоне
        days_difference = (now - start_date).days
        random_days = random.randint(0, days_difference)
        random_date = start_date + timedelta(days=random_days)

        return (
            cls.objects.live()
            .filter(category=category, first_published_at__gte=random_date)
            .exclude(pk=current_page_pk)
            .only('title', 'pub_date', 'main_image', 'author')
            .select_related('main_image')
            .select_related('author')
            .order_by('-first_published_at')[:limit]
        )

        # first_published_at__gte=random_date: выбираются записи, у которых дата публикации (first_published_at)
        # больше или равна (__gte означает "greater than or equal to", то есть "больше или равно")
        # заданной случайной дате random_date.

    @classmethod
    def get_adjacent_materials(cls, current_material):
        # Предыдущий материал: последний из тех, что были опубликованы раньше текущего
        prev_material = cls.objects.live().filter(
            first_published_at__lt=current_material.first_published_at
        ).order_by('-first_published_at').only('title').first()

        # Следующий материал: первый из тех, что были опубликованы позже текущего
        next_material = cls.objects.live().filter(
            first_published_at__gt=current_material.first_published_at
        ).order_by('first_published_at').only('title').first()

        # В Django ORM, фильтры __lt и __gt используются для выборки записей на основе сравнения значений полей.
        # __lt (less than) означает "меньше чем". Когда вы используете этот фильтр,
        # вы запрашиваете записи, в которых значение указанного поля меньше, чем заданное значение.
        # __gt (greater than) означает "больше чем". Этот фильтр используется для выборки записей,
        # где значение поля больше, чем заданное значение.

        return prev_material, next_material

    @classmethod
    def get_top_news(cls, lookback_days=60, limit=5):
        now = timezone.now()
        start_date = now - timedelta(days=lookback_days)

        return (
            cls.objects.live()
            .filter(first_published_at__gte=start_date)
            .only('title', 'pub_date', 'view_count', 'main_image', 'author')
            .select_related('main_image')
            .select_related('author')
            .order_by('-view_count')[:limit]
        )

    @classmethod
    def get_main_materials(cls, limit=5):
        return (
            cls.objects.live()
            .filter(is_main=True)
            .only('title', 'pub_date', 'view_count', 'category', 'main_image', 'author')
            .select_related('category')
            .select_related('main_image')
            .select_related('author')
            .order_by('-first_published_at')[:limit]
        )

    @classmethod
    def get_important_materials(cls, limit=2):
        return (
            cls.objects.live()
            .filter(is_important=True)
            .only('title', 'pub_date', 'view_count', 'category', 'main_image')
            .select_related('category')
            .select_related('main_image')
            .order_by('-first_published_at')[:limit]
        )

    @classmethod
    def get_photo_report_materials(cls, limit):
        return (
            cls.objects.live()
            .annotate(image_count=Count('gallery_images'))
            .filter(
                image_count__gt=1,
                is_photo_report=True
            )
            .order_by('-pub_date')
            .only('title', 'pub_date', 'view_count', 'category', 'main_image')
            .select_related('category')
            .select_related('main_image')[:limit]
        )

    @classmethod
    def get_video_report_materials(cls, limit):
        return (
            cls.objects.live().filter(
                Q(video_url__isnull=False) |
                Q(fb_video_url__isnull=False) |
                Q(video_file__isnull=False)
            ).filter(
                is_video_report=True
            ).order_by('-pub_date')
            .only('title', 'pub_date', 'view_count', 'category', 'main_image')
            .select_related('category')
            .select_related('main_image')[:limit]
        )

    # Возвращает основное(главное) изображение для материала
    # def get_main_image(self):
    #     # noinspection PyUnresolvedReferences
    #     gallery_item = self.gallery_images.first()
    #     # first() возвращает первый объект из виртуального поля gallery_images текущей модели
    #
    #     if gallery_item:
    #         return gallery_item.image
    #     else:
    #         return None

    # Parent page / subpage type rules
    parent_page_types = ['MaterialsIndexPage']
    subpage_types = []

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


# ГАЛЕРЕЯ ИЗОБРАЖЕНИЙ
# Orderable - для создания упорядоченных списков различных типов объектов.
# Например, галерея изображений, список файлов или видео.
class MaterialPageGalleryImage(Orderable):
    # Указываем, что эта галерея будет связана с экземплярами MaterialPage
    # В виртуальном поле 'gallery_images' в экземплярах MaterialPage будет указано(через админку)
    # какие именно изображения из галереи нужно связать с текущем экземпляром MaterialPage
    page = ParentalKey(MaterialPage, on_delete=models.CASCADE, related_name='gallery_images')

    # Для хранения изображений(адреса изображений и служебная информация)
    # в Wagtail есть специальная модель wagtailimages.Image
    # Именно там будут храниться сами изображения из галереи
    # related_name='+' говорит о том, что не нужна обратная связь между этими двумя моделями,
    # и 'wagtailimages.Image' нужна только для хранения изображений
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    caption = models.CharField(verbose_name='Название', blank=True, max_length=250)

    # На странице редактирования материала при добавлении изображения будут отображены эти поля
    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


# Декоратор register_snippet используется для регистрации моделей как сниппетов,
# делая их доступными в админке.
# В контексте Wagtail, сниппеты представляют собой маленькие фрагменты контента,
# которые можно повторно использовать в разных частях сайта. Например Авторы.
@register_snippet
class Author(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=255)
    slug = models.SlugField(max_length=80, unique=True, blank=True, null=True)
    bio = models.TextField(verbose_name="Биография", blank=True, null=True)
    profile_image = models.ImageField("Фото", upload_to='authors/',
                                      help_text="18X18", blank=True, null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('bio'),
        FieldPanel('profile_image')
    ]

    # Этот метод определяет текстовое представление объекта Author,
    # которое будет использоваться, например, при отображении объекта в административной панели.
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Авторы'
        verbose_name_plural = 'Авторы'


@register_snippet
class Category(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    slug = models.SlugField(unique=True, max_length=80)
    is_basic = models.BooleanField(default=False, verbose_name="Основная категория",
                                   help_text="Если выбрать, категория будет отображаться в списке основных категорий")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('is_basic'),
        FieldPanel('sort_order'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


@register_snippet
class RegionCategory(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    slug = models.SlugField(unique=True, max_length=80)
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('sort_order'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
