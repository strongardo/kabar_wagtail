from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import requests
from django.conf import settings


def get_active_category(context):
    from .models import MaterialPage, CategoryPage

    # .get() пытается получить значение по ключу page, но если ключ отсутствует, возвращает None
    # (или другое значение, указанное в качестве второго аргумента), вместо того чтобы выбрасывать KeyError.
    current_page = context.get('page')
    current_category = context.get('current_category')

    # Проверяем, является ли текущая страница материалом и имеет ли она категорию
    if isinstance(current_page, MaterialPage) and hasattr(current_page, 'category'):
        return current_page.category
    # Если current_category есть в текущем контексте (она там может быть, если открывается экземпляр CategoryPage)
    # Она добавляется туда в представлении materials_by_category класса CategoryPage
    elif isinstance(current_page, CategoryPage) and current_category:
        return current_category


def get_paginated_page(queryset, page_number, per_page=3):
    # Создание объекта Paginator, который разбивает queryset (набор данных) на части
    # по per_page объектов на каждой странице
    paginator = Paginator(queryset, per_page)

    try:
        page_number = int(page_number)  # Убедитесь, что page_number является целым числом
    except ValueError:
        page_number = 1  # Если преобразование не удалось, используем номер страницы по умолчанию

    try:
        # Попытка получить объекты для указанного номера страницы из paginator.
        # Если номер страницы корректен, возвращает объект Page с материалами для этой страницы
        return paginator.page(page_number)
    except EmptyPage:
        # Если page_number больше, чем общее количество страниц, вернуть последнюю
        return paginator.page(paginator.num_pages)

# def get_currency_rates_currencyapi():
#     url = f"https://api.currencyapi.com/v3/latest?apikey={settings.CURRENCYAPI_KEY}&base_currency=KGS&currencies=USD,EUR,RUB,KZT"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Вызовет исключение при ошибке HTTP
#         data = response.json()
#         # Предполагая, что структура ответа содержит 'data' с курсами валют
#         rates = data.get('data', {})
#         currency_rates = {currency: info['value'] for currency, info in rates.items()}
#
#         return {currency: 1 / rate for currency, rate in currency_rates.items()}
#     except requests.RequestException as e:
#         print(f"Ошибка при запросе к CurrencyAPI: {e}")
#         return {}
