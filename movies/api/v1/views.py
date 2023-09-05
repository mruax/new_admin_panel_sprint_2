from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, Value
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']  # Список методов, которые реализует обработчик

    def get_queryset(self):
        queryset = Filmwork.objects.values(
            'id', 'title', 'description', 'creation_date', 'rating', 'type'
        ).annotate(
            genres=ArrayAgg(
                Coalesce('genres__name', Value('')),
                distinct=True,
            ),
            actors=ArrayAgg(
                Coalesce('persons__full_name', Value('')),
                filter=Q(personfilmwork__role='actor') & ~Q(persons__full_name=None) & ~Q(persons__full_name=''),
                distinct=True,
            ),
            directors=ArrayAgg(
                Coalesce('persons__full_name', Value('')),
                filter=Q(personfilmwork__role='director') & ~Q(persons__full_name=None) & ~Q(persons__full_name=''),
                distinct=True,
            ),
            writers=ArrayAgg(
                Coalesce('persons__full_name', Value('')),
                filter=Q(personfilmwork__role='writer') & ~Q(persons__full_name=None) & ~Q(persons__full_name=''),
                distinct=True,
            ),
        )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        # TODO: можно ли  использовать dumps (к примеру только в debug) или это повысит нагрузку?
        # и связано ли это с примером вывода в swagger
        return JsonResponse(context, json_dumps_params={'indent': 4})


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset)
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        filmwork = kwargs["object"]
        context = {
            "id": str(filmwork["id"]),
            "title": filmwork["title"],
            "description": filmwork["description"],
            "creation_date": filmwork["creation_date"],
            "rating": filmwork["rating"],
            "type": filmwork["type"],
            "genres": filmwork["genres"],
            "actors": filmwork["actors"],
            "directors": filmwork["directors"],
            "writers": filmwork["writers"]
        }
        return context
