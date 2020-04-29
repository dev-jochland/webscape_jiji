from django.urls import path
from . import views

app_name = 'jiji_app'
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
]