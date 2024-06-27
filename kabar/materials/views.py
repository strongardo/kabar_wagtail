from django.shortcuts import render
from django.http import JsonResponse
from .models import MaterialPage


def get_material_views(request, material_id):
    # Получаем материал по ID и его количество просмотров
    try:
        material = MaterialPage.objects.only('view_count').get(id=material_id)
        views_count = material.view_count
    except MaterialPage.DoesNotExist:
        views_count = 0

    # Возвращаем количество просмотров в формате JSON
    return JsonResponse({'views_count': views_count})
