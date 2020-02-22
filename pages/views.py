from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Page, Category
from django.http import Http404

def index(request):
    return render(request, 'index.html', context={})

def simple_page(request, url):
    page = get_object_or_404(Page, url = url, category=1, active=1)
    return render(request, 'simple_page.html', context={'title':page.title, 'description':page.description})

def category_page(request, category, url):
    category = get_object_or_404(Category, url = category, active=1)
    page = get_object_or_404(Page, url = url, category=category.id, active=1)
    return HttpResponse('category finded')

