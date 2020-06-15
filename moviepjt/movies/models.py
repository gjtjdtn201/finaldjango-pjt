from django.db import models
from django.conf import settings
# Create your models here.

class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    gen_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_gens", blank=True)
    def __str__ (self):
        return self.name

# class Director(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=100)
#     def __str__ (self):
#         return self.name

class Actor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    profile_path = models.CharField(max_length=150)
    def __str__ (self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=150)
    movie_id = models.IntegerField()
    # backdrop_path = models.CharField(max_length=150)
    voteavg = models.IntegerField()
    overview = models.TextField()
    original_title = models.CharField(max_length=100, default='')
    release_date = models.CharField(max_length=50)
    # 감독은 한명만 할꺼니 1:1
    # mdirector = models.ForeignKey(Director, on_delete=models.CASCADE)
    # 영화배우와 장르는 N:M 연결
    actors = models.ManyToManyField(Actor, related_name = 'movie_actor') 
    genres = models.ManyToManyField(Genre, related_name = 'movie_genre')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_movies", blank=True)

    def __str__(self):
        return self.title
    