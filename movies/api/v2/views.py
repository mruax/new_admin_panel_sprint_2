from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models
from django.db.models import Case, When
from django.http import JsonResponse
from django.views.generic.list import BaseListView

from movies.models import Filmwork


class MoviesListApi(BaseListView):
    model = Filmwork
    http_method_names = ['get']  # Список методов, которые реализует обработчик
    paginate_by = 100

    def get_queryset(self):
        queryset = Filmwork.objects.annotate(
            genre_names=ArrayAgg('genres__name', distinct=True),
            actors=ArrayAgg(
                Case(
                    When(personfilmwork__role='actor', then='persons__full_name'),
                    default=None,
                    output_field=models.CharField(),
                ),
                distinct=True,
            ),
            directors=ArrayAgg(
                Case(
                    When(personfilmwork__role='director', then='persons__full_name'),
                    default=None,
                    output_field=models.CharField(),
                ),
                distinct=True,
            ),
            writers=ArrayAgg(
                Case(
                    When(personfilmwork__role='writer', then='persons__full_name'),
                    default=None,
                    output_field=models.CharField(),
                ),
                distinct=True,
            ),
        ).values(
            'id', 'title', 'description', 'creation_date', 'rating', 'type', 'genre_names', 'actors',
            'directors', 'writers'
        )
        return queryset

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

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context, json_dumps_params={'indent': 4})
