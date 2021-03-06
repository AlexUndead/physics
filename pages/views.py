from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Page
from django.http import Http404


def index(request):
    return render(request, 'index.html', context={})


def simple_page(request, url):
    page = get_object_or_404(Page, url=url, active=1)
    return render(request, 'simple_page.html', context={'title': page.title, 'description': page.description})


