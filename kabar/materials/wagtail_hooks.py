from wagtail import hooks
from django.db.models import F
from .models import MaterialPage
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from django.utils.formats import date_format


# Обработчик (хук) для события before_serve_page в Wagtail. Событие before_serve_page срабатывает непосредственно
# перед тем, как страница будет отдана на рендеринг клиенту. Это означает, что функция increment_view_count будет
# вызываться каждый раз, когда какая-либо страница готовится к отображению пользователю.
@hooks.register("before_serve_page")
def increment_view_count(page, request, serve_args, serve_kwargs):
    # Проверка на то, что работаем только с экземплярами MaterialPage
    if isinstance(page.specific, MaterialPage):
        MaterialPage.objects.filter(pk=page.pk).update(view_count=F('view_count') + 1)
        # Увеличение счетчика просмотров для страницы. Используется Django QuerySet API для фильтрации объектов
        # MaterialPage по первичному ключу (pk) текущей страницы (page). Далее применяется метод .update(),
        # который обновляет поле view_count, увеличивая его на 1. Для инкремента используется F-выражение,
        # которое позволяет изменять поля на стороне базы данных напрямую, не извлекая объекты в память, что делает
        # операцию более эффективной и предотвращает проблемы с конкуренцией при одновременных обновлениях.


class MaterialPageAdmin(ModelAdmin):
    model = MaterialPage
    menu_label = 'Материалы'
    menu_icon = 'doc-full'
    add_to_settings_menu = False
    list_display = ('title', 'pub_date')
    # list_editable = ('title', 'pub_date',)


modeladmin_register(MaterialPageAdmin)
