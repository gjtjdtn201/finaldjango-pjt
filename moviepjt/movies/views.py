from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
import requests

MYKEY = '2e55b602956681cb520a7d64930d1274'
n = 1

def takeGenre(request):
    genreURL = f'https://api.themoviedb.org/3/genre/movie/list?api_key={MYKEY}&language=ko-KR'
    genreList = requests.get(genreURL)
    genreDatas = genreList.json().get('genres')
    for genreData in genreDatas:
        Genre.objects.get_or_create(
            id = genreData.get('id'),
            name = genreData.get('name'))
    return redirect('movies:index')

# 영화 가져오는 로직
def takeMovie(request):
    global n

    # tmp, chk2 = Director.objects.get_or_create(
    #     id = 9999999,
    #     name = '없음'
    # )

    movieURL = f'https://api.themoviedb.org/3/discover/movie?api_key={MYKEY}&language=ko-KR&page={str(n)}'
    movieList = requests.get(movieURL)
    resDatas = movieList.json().get('results')

    for resData in resDatas:
        tmd_id = resData.get('id')
        # 감독 가져오기
        CREDITS_URL = f"https://api.themoviedb.org/3/movie/{tmd_id}/credits?api_key={MYKEY}"
        creditsData = requests.get(CREDITS_URL)
        # crewDatas = creditsData.json().get('crew')
        # chk1 = False
        # for i in range(10):
        #     if crewDatas[i].get('job') == 'Director':
        #         director_name = crewDatas[i].get('name')
        #         director_id = crewDatas[i].get('id')
        #         moviedirector, chk1 = Director.objects.get_or_create(
        #             id = director_id,
        #             name = director_name
        #         )
        #         break
        # # 감독을 못찾았다면 임의값 반환
        # if not chk1:
        #     moviedirector = get_object_or_404(Director, pk=9999999)
        # try:
        #     original = resData.get('original_title')
        # except:
        #     original = resData.get('title')

        # movie는 객체, flag는 생성 되었는지 여부
        movie = Movie.objects.create(
            title = resData.get('title'),
            poster_path = "https://image.tmdb.org/t/p/original"+ resData.get('poster_path'),
            movie_id = tmd_id,
            # backdrop_path = "https://image.tmdb.org/t/p/original" + resData.get('backdrop_path'),
            voteavg = resData.get('vote_average'),
            overview = resData.get('overview'),
            original_title = resData.get('original_title'),
            # mdirector = moviedirector,
            release_date = resData.get('release_date'),
            )

        # 영화배우 추가 파트
        castDatas = creditsData.json().get('cast')
        for i in range(6):
            try:
                actor_name = castDatas[i].get('name')
                actor_id = castDatas[i].get('id')
                profile_path = "https://image.tmdb.org/t/p/w300" + castDatas[i].get('profile_path')
                movieactor, chk3 = Actor.objects.get_or_create(
                    id = actor_id,
                    name = actor_name,
                    profile_path = profile_path
                )
                movie.actors.add(movieactor)
            except:
                continue

        # 장르 추가 파트
        genreItems = resData.get('genre_ids')
        for i in genreItems:
            p1 = get_object_or_404(Genre, pk=i)
            movie.genres.add(p1)
    n += 1
    return redirect('movies:index')

# 아래는 template 페이지
def index(request):
    movies = Movie.objects.order_by('-pk')

    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        gens = request.user.like_gens.all()
        totalcnt = 10
        if gens:
            recommends = []
            cnt = totalcnt//len(gens)
            for j in gens:
                chk = 0
                mgen = j.movie_genre.all()
                for z in mgen:
                    recommends.append({
                    'title': z.title, 
                    'pk': z.pk, 
                    'poster_path':z.poster_path,
                    'genres':z.genres})
                    chk += 1
                    if chk == cnt:
                        break

        else:
            recommends = Movie.objects.order_by('?')[:10]
    else:
        recommends = ''

    # 검색하는 부분
    movie = Movie.objects.all()
    actors = Actor.objects.all()
    if request.method=="GET":
        searchword = request.GET.get('searchword','')
        resultMovie = []
        resultActor = []
        
        if searchword:
            searchMovie = movie.filter(title__icontains=searchword)
            searchActor = actors.filter(name__icontains=searchword)
            for c in range(len(searchMovie)):
                resultMovie.append({
                    'title':searchMovie[c].title, 
                    'id':searchMovie[c].id, 
                    'poster_path':searchMovie[c].poster_path})

            for c in range(len(searchActor)):
                resultActor.append({
                    'name':searchActor[c].name,
                    'id': searchActor[c].id,
                    'profile_path':searchActor[c].profile_path})
            return render(request,'movies/searchresult.html',
            {'resultMovie':resultMovie,'resultActor':resultActor, 'searchword':searchword})

    context = {
        'movies': movies,
        'page_obj' : page_obj,
        'recommends': recommends,
    }
    return render(request, 'movies/index.html', context)

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = movie.review_set.all()
    score = 0
    for i in reviews:
        score += i.rank
    if len(reviews) == 0:
        pass
    else:
        score = round(score/len(reviews),1)
    context = {
        'movie': movie,
        'score': score,
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

# review 생성
@login_required
def review_create(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
        return redirect('movies:review_detail', review.movie.id, review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
        'movie': movie
    }
    return render(request, 'movies/review_form.html', context)

# review 상세조회
def review_detail(request, pk, review_pk):
    movie = get_object_or_404(Movie, pk=pk)
    review = get_object_or_404(Review, pk=review_pk)
    form = CommentForm()
    context = {
        'movie': movie,
        'review': review,
        'form': form,
    }
    return render(request, 'movies/review_detail.html', context)

# review 수정

@login_required
def review_update(request, pk, review_pk):
    movie = get_object_or_404(Movie, pk=pk)
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.movie = movie
                review.save()
                return redirect('movies:review_detail', review.movie.pk, review.pk)
        else:
            form = ReviewForm(instance=review)

        context = {
            'form' : form,
        }
        return render(request, 'movies/review_form.html', context)
    else:
        return redirect('movies:review_detail', review_pk)


## review 삭제
@login_required
@require_POST
def review_delete(request, pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        review.delete()

    return redirect('movies:movie_detail', review.movie.pk)


# comment 생성, require_POST활용
@login_required
@require_POST
def comment_create(request, pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()

    return redirect('movies:review_detail', review.movie.id, review_pk)

# comment 삭제, require_POST활용
@login_required
@require_POST
def comment_delete(request, pk, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()

    return redirect('movies:review_detail', review.movie.id, review_pk)

def actor_idx(request, actor_id):
    actor = Actor.objects.get(id=actor_id)
    context = {
        'actor': actor,
    }
    return render(request, 'movies/actor.html', context)

def community(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews': reviews,
    }
    return render(request, 'movies/community.html', context)