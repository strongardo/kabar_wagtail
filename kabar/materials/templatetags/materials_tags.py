from django import template
from materials.models import Category, RegionCategory, MaterialPage, RegionCategoryPage
from materials.utils import get_active_category

# Код в этом файле создает переиспользуемые шаблонные теги, которые можно вставить в любой шаблон.

# Экземпляр Library, который будет использоваться для регистрации тегов
register = template.Library()


# В шаблоне регистрируемого тега не будет прямого доступа к текущему контексту страницы
# и нужно формировать собственный контекст для этого шаблона.
# Декоратор @register.inclusion_tag регистрирует функцию как inclusion tag,
# позволяя ей возвращать контекст для заданного шаблона.
# 'takes_context=True' означает, что функция принимает текущий контекст страницы.
@register.inclusion_tag('materials/categories_list.html', takes_context=True)
def basic_categories_list(context):
    basic_categories = Category.objects.filter(is_basic=True).order_by('sort_order')[:5]
    # active_category = get_active_category(context)

    # Возвращаем словарь контекста, который будет использоваться в шаблоне 'basic_materials/categories_list.html'
    return {
        # Прямо передаем объект request из текущего контекста для возможного использования в шаблоне
        'request': context['request'],
        # Прямо передаем объект category_page из текущего контекста,
        # который был добавлен в текущий контекст в файле context_processor.py
        'category_page': context['category_page'],  # Для формирования routablepageurl на страницу категории
        'categories': basic_categories,
        # 'active_category': active_category,
    }


@register.inclusion_tag('materials/categories_list.html', takes_context=True)
def regular_categories_list(context):
    regular_categories = Category.objects.filter(is_basic=False).order_by('sort_order')[:7]
    # active_category = get_active_category(context)

    return {
        'request': context['request'],
        'category_page': context['category_page'],
        'categories': regular_categories,
        # 'active_category': active_category,
    }


@register.inclusion_tag('materials/region_categories_list.html', takes_context=True)
def region_categories_list(context):
    region_categories = RegionCategory.objects.all().order_by('sort_order')[:7]

    region_page = RegionCategoryPage.objects.live().only('title', 'slug').first()

    return {
        'request': context['request'],
        'region_page': region_page,
        'region_categories': region_categories,
    }


@register.inclusion_tag('materials/all_categories_list.html', takes_context=True)
def all_categories_list(context):
    categories = Category.objects.all().order_by('sort_order')

    return {
        'request': context['request'],
        'category_page': context['category_page'],
        'categories': categories,
    }


@register.inclusion_tag('materials/blocks/popular_news_item_block.html', takes_context=True)
def popular_news_item_block(context):
    return {
        'post': context['post'],
    }


@register.inclusion_tag('materials/blocks/similar_news_item_block.html', takes_context=True)
def similar_news_item_block(context):
    return {
        'post': context['post'],
    }


@register.inclusion_tag('materials/blocks/mini_news_item_block.html', takes_context=True)
def mini_news_item_block(context):
    return {
        'post': context['post'],
    }
