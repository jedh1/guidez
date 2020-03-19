from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('search/', views.get_search, name = 'search'),
    path('about/', views.about, name = 'about'),
]
