from django.urls import path

from . import views

urlpatterns = [
    path('<slug:category>/<slug:url>/', views.category_page, name='category-page'),
    path('<slug:url>/', views.simple_page, name='simple-page'),
    path('', views.index, name='index'),
]
