from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
    verbose_name = _('Movies')


class FilmworkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filmworks'
    verbose_name = _('Filmworks')


class AppsConfig(AppConfig):
    name = 'movies.apps'  # important to specify full name/path
    verbose_name = _('Applications configuration')

    def ready(self):
        # flake8 needs to ignore F401
        import movies.signals
