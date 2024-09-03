from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.models import Page, models
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.settings.models import (
    BaseGenericSetting,  # настройка для всех сайтов
    BaseSiteSetting,  # настройка для текущего сайтов
    register_setting,
)
from wagtail.snippets.models import register_snippet

from materials.utils import get_paginated_page


class SimplePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = 'Простая страница'


class PressConferenceAnnouncementsPage(RoutablePageMixin, Page):
    # Этот маршрут соответствует базовому URL страницы (/press-conference-announcements/)
    @route(r'^$')
    @route(r'^page_(?P<page_number>\d+)/$')
    def announcements_view(self, request, page_number=1):
        from materials.models import MaterialPage, Category
        announcements = PressConferenceAnnouncement.get_announcements()
        page_obj = get_paginated_page(announcements, page_number, per_page=1)
        press_category = Category.objects.get(slug='press-center')
        press_materials = MaterialPage.get_materials_by_category_with_author(press_category, limit=3)

        return self.render(request, context_overrides={
            'page_obj': page_obj,
            'press_materials': press_materials
        })

    parent_page_types = ['home.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = 'Страница анонсов пресс-конференций'


class PressConferenceAnnouncement(ClusterableModel):
    pub_date = models.DateTimeField("Дата и время пресс-конференции")
    title = models.TextField(
        blank=True,
        null=True,
        default='',
        verbose_name="Название (описание)"
    )

    panels = [
        FieldPanel('pub_date'),
        FieldPanel('title'),
        InlinePanel('participants', label="Участники")
    ]

    @classmethod
    def get_announcements(cls):
        return cls.objects.all()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Анонс пресс-конференции"
        verbose_name_plural = "Анонсы пресс-конференций"


class PressConferenceParticipant(models.Model):
    announcement = ParentalKey(PressConferenceAnnouncement, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(verbose_name="Имя участника", max_length=255)
    position = models.CharField(verbose_name="Должность участника", max_length=255, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('position'),
    ]

    def __str__(self):
        return self.name


# Регистрирует настройку в админке
@register_setting
class CurrencyExchangeRates(BaseSiteSetting):
    dollar_rate = models.DecimalField(verbose_name='Курс доллара', max_digits=10, decimal_places=2, null=True)
    euro_rate = models.DecimalField(verbose_name='Курс евро', max_digits=10, decimal_places=2, null=True)
    tenge_rate = models.DecimalField(verbose_name='Курс тенге', max_digits=10, decimal_places=2, null=True)
    ruble_rate = models.DecimalField(verbose_name='Курс рубля', max_digits=10, decimal_places=2, null=True)

    panels = [
        FieldPanel('dollar_rate'),
        FieldPanel('euro_rate'),
        FieldPanel('tenge_rate'),
        FieldPanel('ruble_rate'),
    ]

    class Meta:
        verbose_name = "Курс валют"


@register_snippet
class OtherLinks(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    url = models.URLField("Ссылка", blank=True, null=True)
    image = models.ImageField("Изображение", upload_to='other_links/', blank=True, null=True,
                              help_text="400X150 или кратно этому")
    is_active = models.BooleanField(default=True, verbose_name="Показать/Скрыть",
                                    help_text="Снимите галочку, чтобы скрыть ссылку на сайте")
    sort_order = models.PositiveIntegerField("Порядок сортировки", default=0)

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
        FieldPanel('image'),
        FieldPanel('is_active'),
        FieldPanel('sort_order'),
    ]

    @classmethod
    def get_other_links(cls):
        return (
            cls.objects
            .filter(is_active=True)
            .only('name', 'url', 'image')
            .order_by('sort_order')
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сторонняя ссылка'
        verbose_name_plural = 'Сторонние ссылки'


@register_snippet
class Partners(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    url = models.URLField("Ссылка", blank=True, null=True)
    image = models.ImageField("Изображение", upload_to='other_links/', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Показать/Скрыть",
                                    help_text="Снимите галочку, чтобы скрыть партнера на сайте")
    sort_order = models.PositiveIntegerField("Порядок сортировки", default=0)

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
        FieldPanel('image'),
        FieldPanel('is_active'),
        FieldPanel('sort_order'),
    ]

    @classmethod
    def get_partners(cls):
        return (
            cls.objects
            .filter(is_active=True)
            .only('name', 'url', 'image')
            .order_by('sort_order')
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'


class Banner(models.Model):
    POSITION_CHOICES = [
        ('main', 'Главная страница'),
        ('aside', 'Боковая колонка'),
    ]

    title = models.CharField(verbose_name='Название', max_length=255)
    image = models.ForeignKey(
        'wagtailimages.Image', verbose_name='Изображение',
        null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    url = models.URLField(verbose_name='Ссылка', max_length=500, blank=True)
    position = models.CharField(verbose_name='Позиция', max_length=20, choices=POSITION_CHOICES)
    views = models.PositiveIntegerField(verbose_name='Просмотры', default=0)
    clicks = models.PositiveIntegerField(verbose_name='Клики', default=0)

    panels = [
        FieldPanel('title'),
        FieldPanel('image'),
        FieldPanel('url'),
        FieldPanel('position'),
    ]

    @classmethod
    def get_banners(cls, pos):
        return (
            cls.objects
            .filter(position=pos)
            .only('title', 'image')
            .select_related('image')
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"
