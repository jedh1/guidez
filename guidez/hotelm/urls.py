from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('search/', views.get_search, name = 'search'),
    path('about/', views.about, name = 'about'),
    path('register/', views.register, name = 'register'),
    path('login/', views.login_request, name = 'login'),
    path('logout/', views.logout_request, name = 'logout'),
]
