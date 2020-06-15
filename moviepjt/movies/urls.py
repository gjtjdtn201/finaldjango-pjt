from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('takeGenre/', views.takeGenre),
    path('takeMovie/', views.takeMovie),
    path('movie_create/', views.movie_create, name='movie_create'),
    path('<int:pk>/', views.movie_detail, name='movie_detail'),
    path('<int:pk>/delete/', views.movie_delete, name='movie_delete'),
    path('<int:pk>/update/', views.movie_update, name='movie_update'),
    path('<int:pk>/like/', views.like, name="like"),
    path('<int:pk>/review_create/', views.review_create, name='review_create'),
    path('<int:pk>/<int:review_pk>/', views.review_detail, name='review_detail'),
    path('<int:pk>/<int:review_pk>/delete/', views.review_delete, name='review_delete'),
    path('<int:pk>/<int:review_pk>/update/', views.review_update, name='review_update'),
    path('<int:pk>/<int:review_pk>/comments/', views.comment_create, name='comment_create'),
    path('<int:pk>/<int:review_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:pk>/<int:review_pk>/like/', views.like, name="like"),
    path('actor/<int:actor_id>', views.actor_idx, name='actor_idx'),

    ]