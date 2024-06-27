from django.urls import path
from .views import get_material_views

urlpatterns = [
    path('get_views/<int:material_id>/', get_material_views, name='get-material-views'),
]
