from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns=[
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('detail/<str:username>/', views.detail, name='detail'),
    path('<str:username>/follow', views.follow, name='follow'),
    path('<int:pk>/genlike/', views.genlike, name="genlike"),
    ]