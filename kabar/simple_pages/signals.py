from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import CurrencyExchangeRates, OtherLinks, Partners
from materials.models import Category
from django.core.cache.utils import make_template_fragment_key


@receiver(post_save, sender=CurrencyExchangeRates)
def clear_currency_rates_cache(sender, instance, **kwargs):
    key = make_template_fragment_key("currencyexchangerates")
    cache.delete(key)


@receiver(post_save, sender=Category)
def clear_basic_categories_cache(sender, instance, **kwargs):
    key = make_template_fragment_key("basic_categories")
    cache.delete(key)


@receiver(post_save, sender=Category)
def clear_regular_categories_cache(sender, instance, **kwargs):
    key = make_template_fragment_key("regular_categories")
    cache.delete(key)


@receiver(post_save, sender=Category)
def clear_mobile_nav_cache(sender, instance, **kwargs):
    key = make_template_fragment_key("mobile_nav")
    cache.delete(key)


@receiver(post_save, sender=OtherLinks)
def clear_other_links_cache(sender, instance, **kwargs):
    key = make_template_fragment_key("other_links")
    cache.delete(key)


@receiver(post_save, sender=Partners)
def clear_partners_cache(sender, instance, **kwargs):
    key = make_template_fragment_key("partners")
    cache.delete(key)
