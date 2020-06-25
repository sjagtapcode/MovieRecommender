import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','movier.settings')

from django.contrib.postgres.fields import ArrayField

import django
django.setup()

from app.models import Movies
import requests

api_key="1a5e0388c846644ea8969c931955d996"
# res=requests.get('http://api.themoviedb.org/3/trending/movie/week?api_key='+api_key)
#
# data=res.json()
# for r in data["results"]:
#     Movies.objects.create(
#     mid = r["id"],
#     vote_count = r["vote_count"],
#     vote_average = r["vote_average"],
#     release_date = r["release_date"],
#     language = r["original_language"],
#     title = r["original_title"],
#     adult = r["adult"],
#     popularity = r["popularity"],
#     poster_path = r["poster_path"],
#     genre_ids = r["genre_ids"],
#     overview = r["overview"],
#     )

def complete():
    res=requests.get('https://api.themoviedb.org/3/discover/movie?api_key='+api_key+'&sort_by=release_date.desc&include_adult=false&include_video=false')
    data=res.json()
    pages=data["total_pages"]
    count=data["total_results"]
    cnt=0
    print(pages)
    for i in range(1,20):
        print(str(i))
        # res=requests.get('https://api.themoviedb.org/3/discover/movie?api_key='+api_key+'&sort_by=release_date.desc&include_adult=false&include_video=false&page='+str(i))
        res=requests.get('https://api.themoviedb.org/3/movie/popular?api_key='+api_key+'&language=en-US&page='+str(i))
        data=res.json()
        for r in data["results"]:
            cnt=cnt+1
            if r["original_language"]=="en":
                Movies.objects.get_or_create(
                mid = r["id"],
                vote_count = r["vote_count"],
                vote_average = r["vote_average"],
                release_date = r["release_date"],
                language = r["original_language"],
                title = r["original_title"],
                adult = r["adult"],
                popularity = r["popularity"],
                poster_path = r["poster_path"],
                genre_ids = r["genre_ids"],
                overview = r["overview"],
                )
    print("number of entries = "+ str(cnt))

complete()

#
# res=requests.get('https://api.themoviedb.org/3/discover/movie?api_key='+api_key+'&sort_by=release_date.desc&include_adult=false&include_video=false&page=2')
# data=res.json()
# print(data["total_pages"])
# for r in data["results"]:
#     Movies.objects.create(
#     mid = r["id"],
#     vote_count = r["vote_count"],
#     vote_average = r["vote_average"],
#     release_date = r["release_date"],
#     language = r["original_language"],
#     title = r["original_title"],
#     adult = r["adult"],
#     popularity = r["popularity"],
#     poster_path = r["poster_path"],
#     genre_ids = r["genre_ids"],
#     overview = r["overview"],
#     )
