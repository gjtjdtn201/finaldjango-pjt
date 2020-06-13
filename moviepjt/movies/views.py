from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
import requests

# 영화 가져오는 로직
def takeMovie(request):

    MYKEY = '2e55b602956681cb520a7d64930d1274'

    genreURL = f'https://api.themoviedb.org/3/genre/movie/list?api_key={MYKEY}&language=ko-KR'
    genreList = requests.get(genreURL)
    genreDatas = genreList.json().get('genres')
    for genreData in genreDatas:
        Genre.objects.get_or_create(
            id = genreData.get('id'),
            name = genreData.get('name'))
    # tmp, chk2 = Director.objects.get_or_create(
    #     id = 9999999,
    #     name = '없음'
    # )
    for n in range(1, 7):
        movieURL = f'https://api.themoviedb.org/3/discover/movie?api_key={MYKEY}&language=ko-KR&page={str(n)}'
        movieList = requests.get(movieURL)
        resDatas = movieList.json().get('results')

        for resData in resDatas:
            # tmd_id = resData.get('id'),
            # 감독 가져오기
            # CREDITS_URL = f"https://api.themoviedb.org/3/movie/{tmd_id}/credits?api_key={MYKEY}"
            # creditsData = requests.get(CREDITS_URL)
            # crewDatas = creditsData.json().get('crew')
            # chk1 = False
            # for i in range(10):
            #     if crewDatas[i].get('job') == 'Director':
            #         director_name = crewDatas[i].get('name')
            #         director_id = crewDatas[i].get('id')
            #         moviedirector, chk1 = crewDatas.objects.get_or_create(
            #             id = director_id,
            #             name = director_name
            #         )
            #         break

            # movie는 객체, flag는 생성 되었는지 여부
            movie, flag = Movie.objects.get_or_create(
                title = resData.get('title'),
                poster_path = "https://image.tmdb.org/t/p/original"+ resData.get('poster_path'),
                movie_id = resData.get('id'),
                # backdrop_path = "https://image.tmdb.org/t/p/original" + resData.get('backdrop_path'),
                voteavg = resData.get('vote_average'),
                overview = resData.get('overview'),
                # original_title = resData.get('orginal_title'),
                release_date = resData.get('release_date'),
                )
            # if chk1:
            #     movie.director.add(moviedirector)
            # else:
            #     movie.director.add(tmp)
            genreItems = resData.get('genre_ids')
            for i in genreItems:
                p1 = get_object_or_404(Genre, pk=i)
                movie.genres.add(p1)
    
    return redirect('movies:index')

# 아래는 template 페이지
def index(request):
    movies = Movie.objects.order_by('-pk')

    paginator = Paginator(movies, 12)
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
    # genres = movie.genres.all()
    context = {
        'movie': movie,
        # 'genres': genres,
    }
    # print(genres)
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
