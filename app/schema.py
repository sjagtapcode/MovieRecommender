import graphene
from graphene_django import DjangoObjectType

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Movies,Lists


class MovieType(DjangoObjectType):
    class Meta:
        model = Movies


class MovieTitleType(DjangoObjectType):
    class Meta:
        model = Movies
        fields = ('mid','title')


class ListType(DjangoObjectType):
    class Meta:
        model = Lists


class MoviePaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(MovieTitleType)


class Query(graphene.ObjectType):
    all_movies = graphene.List(
        MoviePaginatedType,
        page=graphene.Int()
    )
    single_movie = graphene.List(
        MovieType,
        id=graphene.Int()
    )
    all_lists = graphene.List(ListType)

    def resolve_single_movie(self, info, id, **kwargs):
        return {Movies.objects.get(mid=id)}

    def resolve_all_lists(self, args):
        return Lists.objects.all()

    def resolve_all_movies(self, info, page, **kwargs):
        page_size = 20
        if page == 0:
            page=1
        qs = Movies.objects.all()
        skip = page_size*(page-1)
        num_pages=qs.count()/page_size
        qs = qs[skip:skip+page_size]
        print(qs.count())
        has_next=True
        has_previous = True
        if page == num_pages:
            has_next = False
        if page == 1:
            has_previous = False
        return {MoviePaginatedType(
            page = page,
            pages = num_pages,
            has_next = has_next,
            has_prev = has_previous,
            objects = qs,
            **kwargs
        )}


