from django import template

register = template.Library()


@register.inclusion_tag('home/blocks/late_news_extra_block.html', takes_context=True)
def late_news_extra_block(context):
    return {
        'post': context['post'],
    }


@register.inclusion_tag('home/blocks/late_news_slide_block.html', takes_context=True)
def late_news_slide_block(context):
    return {
        'post': context['post'],
    }


@register.inclusion_tag('home/blocks/news_feed_item_block.html', takes_context=True)
def news_feed_item_block(context):
    return {
        'post': context['post'],
    }


@register.inclusion_tag('home/blocks/_news_data_inner_author.html', takes_context=True)
def news_data_inner_author(context):
    return {
        'post': context['post'],
    }


@register.inclusion_tag('home/blocks/_news_data_inner.html', takes_context=True)
def news_data_inner(context):
    return {
        'post': context['post'],
    }


@register.inclusion_tag('home/blocks/popular_news_item_block.html', takes_context=True)
def popular_news_item_block(context):
    return {
        'post': context['post'],
    }


@register.inclusion_tag('home/blocks/multiple_news_main_block.html', takes_context=True)
def multiple_news_main_block(context):
    return {
        'post': context['post'],
    }


@register.inclusion_tag('home/blocks/multiple_news_block.html', takes_context=True)
def multiple_news_block(context):
    return {
        'post': context['post'],
    }


@register.inclusion_tag('home/blocks/mini_news_item_block.html', takes_context=True)
def mini_news_item_block(context):
    return {
        'post': context['post'],
    }


@register.inclusion_tag('home/blocks/primary_news_item_block.html', takes_context=True)
def primary_news_item_block(context):
    return {
        'post': context['post'],
    }


@register.inclusion_tag('home/blocks/other_links_item_block.html', takes_context=True)
def other_links_item_block(context):
    return {
        'post': context['post'],
    }


@register.inclusion_tag('home/blocks/partners_slide_block.html', takes_context=True)
def partners_slide_block(context):
    return {
        'post': context['post'],
    }
