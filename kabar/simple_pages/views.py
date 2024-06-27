from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F
from .models import Banner


def banner_click(request, banner_id):
    banner = get_object_or_404(Banner, pk=banner_id)
    Banner.objects.filter(pk=banner.id).update(clicks=F('clicks') + 1)
    return redirect(banner.url)
