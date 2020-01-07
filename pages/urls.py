from django.urls import path

from . import views

urlpatterns = [
    path('<slug:url>', views.simple_page, name='simple-page'),
    path('', views.index, name='index'),
]
