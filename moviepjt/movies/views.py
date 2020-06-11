from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Movie, Genre
from .forms import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
import requests

# 영화 가져오는 로직
def takeMovie(request):

    MYKEY = '2e55b602956681cb520a7d64930d1274'

    for n in range(1, 7):
        movieURL = f'https://api.themoviedb.org/3/discover/movie?api_key={MYKEY}&language=ko-KR&page={str(n)}'
        movieList = requests.get(movieURL)
        resDatas = movieList.json().get('results')

        for resData in resDatas:
            Movie.objects.get_or_create(
                title = resData.get('title'),
                poster_path = "https://image.tmdb.org/t/p/original"+ resData.get('poster_path'),
                movie_id = resData.get('id'),
                backdrop_path = "https://image.tmdb.org/t/p/original" + resData.get('backdrop_path'),
                voteavg = resData.get('vote_average'),
                overview = resData.get('overview'),
                original_title = resData.get('orginal_title'),
                release_date = resData.get('release_date'),
            )
    return render(request, 'movies/index.html')

# 아래는 template 페이지
def index(request):
    movies = Movie.objects.order_by('-pk')

    paginator = Paginator(movies, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    recommends = Movie.objects.order_by('?')[:10]
    context = {
        'movies': movies,
        'page_obj' : page_obj,
        'recommends': recommends,
    }
    return render(request, 'movies/index.html', context)

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    genres = movie.genres.all()
    context = {
        'movie': movie,
        'genres': genres,
    }
    return render(request, 'movies/movie_detail.html', context)

@user_passes_test(lambda u: u.is_superuser)
@login_required
def movie_create(request):
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = MovieForm()
    context = {
        'form': form
    }
    return render(request, 'movies/form.html', context)

@user_passes_test(lambda u: u.is_superuser)
@login_required
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()

    return redirect('movies:index')

@user_passes_test(lambda u: u.is_superuser)
@login_required
def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:movie_detail', movie.pk)
    else:
        form = MovieForm(instance=movie)
    context = {
        'form': form
    }
    return render(request, 'movies/form.html', context)


def like(request, pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=pk)

    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        liked = False
    else:
        movie.like_users.add(user)
        liked =True
    context ={
        'liked' : liked,
        'count' : movie.like_users.count(),
    }

    return JsonResponse(context)
