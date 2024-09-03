import random

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import F
from django.template.response import TemplateResponse

from materials.models import MaterialPage
from simple_pages.models import Banner


# To enable logging of search queries for use with the "Promoted search results" module
# <https://docs.wagtail.org/en/stable/reference/contrib/searchpromotions.html>
# uncomment the following line and the lines indicated in the search function
# (after adding wagtail.contrib.search_promotions to INSTALLED_APPS):

# from wagtail.contrib.search_promotions.models import Query


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Search
    if search_query:
        # search_results = Page.objects.live().search(search_query)
        search_results = MaterialPage.get_materials().search(search_query)

        # To log this query for use with the "Promoted search results" module:

        # query = Query.get(search_query)
        # query.add_hit()

    else:
        search_results = MaterialPage.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    # Banners
    banners = list(Banner.get_banners(pos='aside'))
    selected_banners = random.sample(banners, min(len(banners), 2))
    first_banner = selected_banners[0] if len(selected_banners) > 0 else None
    second_banner = selected_banners[1] if len(selected_banners) > 1 else None
    if first_banner:
        Banner.objects.filter(pk=first_banner.pk).update(views=F('views') + 1)
    if second_banner:
        Banner.objects.filter(pk=second_banner.pk).update(views=F('views') + 1)

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "page_obj": search_results,
            'first_banner': first_banner,
            'second_banner': second_banner,
        },
    )
