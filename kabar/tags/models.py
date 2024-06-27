from django.db import models
from wagtail.models import Page
from materials.models import MaterialPage


class TagPage(Page):
    def get_context(self, request):
        # Получаем значение параметра 'tag' из строки запроса.
        # Это позволяет определить, какой тег был выбран для фильтрации материалов.
        tag = request.GET.get('tag')
        materials = MaterialPage.objects.live().order_by('-first_published_at').filter(tags__name=tag)

        context = super().get_context(request)
        # Добавляем в стандартный контекст, отфильтрованные по тегу материалы
        context['materialpages'] = materials

        return context

    parent_page_types = ['home.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = 'Страница тега'
