from django.contrib import admin

from publications.models import Publication
from publications.models import Category 

admin.site.register(Publication)
admin.site.register(Category)
