from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import Http404
from .models import Publication

def publications_index(request):
    return render(request, 'publications_index.html', context={})

def publications_simple_page(request, url):
    publication = get_object_or_404(Publication, url = url, category=1, active=1)
    return render(request, 'publications_simple_page.html', context={
        "title":publication.title,
        "description":publication.description
    })
