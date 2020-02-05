from django.urls import path

from . import views

urlpatterns = [
    path('', views.publications_index, name='publications_index'),
    path('<slug:url>/', views.publications_simple_page, name='publications_simple_page'),
]
