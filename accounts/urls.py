from django.urls import path
from . import views
from .views import search_movies_view


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('users/', views.get_users, name='get_users'),
    path('search/', search_movies_view, name='search_movies'),

]
