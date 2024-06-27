from wagtail.models import Page, models
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import (
    BaseGenericSetting,  # настройка для всех сайтов
    BaseSiteSetting,  # настройка для текущего сайтов
    register_setting,
)


class SimplePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = 'Простая страница'


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


class Banner(models.Model):
    POSITION_CHOICES = [
        ('header', 'Шапка'),
        ('main_top', 'Главная сверху'),
        ('main_bottom', 'Главная снизу'),
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
    def get_banners(cls):
        return cls.objects.only('title', 'image', 'position').select_related('image')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"
