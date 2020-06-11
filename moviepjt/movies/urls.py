from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('takeMovie/', views.takeMovie),
    path('movie_create/', views.movie_create, name='movie_create'),
    path('<int:pk>/', views.movie_detail, name='movie_detail'),
    path('<int:pk>/delete/', views.movie_delete, name='movie_delete'),
    path('<int:pk>/update/', views.movie_update, name='movie_update'),
    path('<int:pk>/like/', views.like, name="like"),

    ]