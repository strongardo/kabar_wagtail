from django.urls import path
from .views import banner_click

urlpatterns = [
    path('banner_click/<int:banner_id>/', banner_click, name='banner_click'),
]
