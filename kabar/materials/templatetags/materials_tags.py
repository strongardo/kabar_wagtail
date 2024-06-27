from django import template
from materials.models import Category, MaterialPage
from materials.utils import get_active_category

# Код в этом файле создает переиспользуемые шаблонные теги, которые можно вставить в любой шаблон.

# Экземпляр Library, который будет использоваться для регистрации тегов
register = template.Library()


# В шаблоне регистрируемого тега не будет прямого доступа к текущему контексту страницы
# и нужно формировать собственный контекст для этого шаблона.
# Декоратор @register.inclusion_tag регистрирует функцию как inclusion tag,
# позволяя ей возвращать контекст для заданного шаблона.
# 'takes_context=True' означает, что функция принимает текущий контекст страницы.
@register.inclusion_tag('materials/basic_categories_list.html', takes_context=True)
def basic_categories_list(context):
    categories = Category.objects.filter(is_basic=True)
    active_category = get_active_category(context)

    # Возвращаем словарь контекста, который будет использоваться в шаблоне 'basic_materials/categories_list.html'
    return {
        # Прямо передаем объект request из текущего контекста для возможного использования в шаблоне
        'request': context['request'],
        # Прямо передаем объект category_page из текущего контекста,
        # который был добавлен в текущий контекст в файле context_processor.py
        'category_page': context['category_page'],  # Для формирования routablepageurl на страницу категории
        'categories': categories,
        'active_category': active_category,
    }


@register.inclusion_tag('materials/regular_categories_list.html', takes_context=True)
def regular_categories_list(context):
    categories = Category.objects.exclude(is_basic=True)
    active_category = get_active_category(context)

    return {
        'request': context['request'],
        'category_page': context['category_page'],
        'categories': categories,
        'active_category': active_category,
    }


@register.inclusion_tag('materials/top_news_list.html', takes_context=True)
def top_news_list(context):
    top_news = MaterialPage.get_top_news()

    return {
        'request': context['request'],
        'top_news': top_news
    }
