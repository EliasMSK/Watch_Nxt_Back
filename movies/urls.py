from django.urls import path
from . import views

urlpatterns = [
    path('search-movies/', views.search_movies_api, name='search_movies_api'),
    path('get-all-movies/', views.get_all_movies_api, name='get_all_movies_api'),
    path('create-movie/', views.create_movie, name='create_movie'),
    path('update-movie/<int:pk>/', views.update_movie, name='update_movie'),
    path('delete-movie/<int:pk>/', views.delete_movie, name='delete_movie'),
]
