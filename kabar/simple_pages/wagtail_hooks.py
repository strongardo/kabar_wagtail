from wagtail import hooks
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import Banner


# Таким образом можно зарегистрировать в админке лоюбую простую модель
class BannerAdmin(ModelAdmin):
    model = Banner
    menu_label = 'Баннеры'
    menu_icon = 'image'
    add_to_settings_menu = False
    list_display = ('title', 'views', 'clicks')
    list_editable = ('title', 'image', 'url', 'position')


modeladmin_register(BannerAdmin)


@hooks.register('construct_main_menu')
def customize_menu_items(request, menu_items):
    # Определяем, имеет ли пользователь статус администратора или модератора
    is_admin = request.user.is_superuser
    is_moderator = request.user.groups.filter(name='Moderators').exists()

    # Если пользователь не является администратором или модератором,
    # скрываем пункты "Отчеты", "Страницы" и "Помощь"
    if not (is_admin or is_moderator):
        menu_items[:] = [item for item in menu_items if item.name not in ['reports', 'explorer', 'help']]

    for item in menu_items:
        if item.name == 'documents':
            item.label = 'Документы и видео'
