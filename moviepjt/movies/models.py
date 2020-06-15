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
    poster_path = models.CharField(max_length=150, default='')
    movie_id = models.IntegerField()
    # backdrop_path = models.CharField(max_length=150)
    voteavg = models.IntegerField(default=0)
    overview = models.TextField(default='')
    original_title = models.CharField(max_length=100, null=True)
    release_date = models.CharField(max_length=50)
    # 감독은 한명만 할꺼니 1:1
    # mdirector = models.ForeignKey(Director, on_delete=models.CASCADE)
    # 영화배우와 장르는 N:M 연결
    actors = models.ManyToManyField(Actor, related_name = 'movie_actor') 
    genres = models.ManyToManyField(Genre, related_name = 'movie_genre')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_movies", blank=True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    title = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rank = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)