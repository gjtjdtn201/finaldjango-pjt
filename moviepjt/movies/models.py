from django.db import models
from django.conf import settings
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=150)
    gen_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_gens", blank=True)
    def __str__ (self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=150)
    movie_id = models.CharField(max_length=50)
    backdrop_path = models.CharField(max_length=150)
    voteavg = models.IntegerField()
    overview = models.TextField()
    # original_title = models.CharField(max_length=100, blank=True)
    release_date = models.CharField(max_length=50)
    # director = models.CharField(max_length=100)

    genres = models.ManyToManyField(Genre, related_name = 'movie_genre')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_movies", blank=True)

    def __str__(self):
        return self.title
    