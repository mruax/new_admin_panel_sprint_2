from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Register your models here.
from movies.models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork

from django.utils.text import Truncator


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description', 'created_at', 'updated_at')
    search_fields = ('name',)

    def short_description(self, obj):
        return Truncator(obj.description).chars(40, truncate='...')

    short_description.short_description = _('Description')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,)
    list_display = ('full_name', 'created_at', 'updated_at')
    search_fields = ('full_name',)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)
    list_display = ('title', 'type', 'creation_date', 'rating', 'created_at', 'updated_at',)
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id',)
