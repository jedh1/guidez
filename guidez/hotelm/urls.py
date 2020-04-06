from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
    path('history/', views.history, name = 'history'),
    path('login/', views.login_request, name = 'login'),
    path('logout/', views.logout_request, name = 'logout'),
    path('register/', views.register, name = 'register'),
    path('search/', views.get_search, name = 'search'),
    path('delete_search/', views.delete_search, name = 'delete_search'),
]
