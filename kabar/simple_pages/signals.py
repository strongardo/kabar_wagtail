from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import CurrencyExchangeRates
from materials.models import Category
from django.core.cache.utils import make_template_fragment_key


@receiver(post_save, sender=CurrencyExchangeRates)
def clear_currency_rates_cache(sender, instance, **kwargs):
    key = make_template_fragment_key("currencyexchangerates")
    cache.delete(key)


@receiver(post_save, sender=Category)
def clear_navigation_cache(sender, instance, **kwargs):
    key = make_template_fragment_key("navigation")
    cache.delete(key)
