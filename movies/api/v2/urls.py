from django.urls import path

from movies.api.v2 import views

urlpatterns = [
    # path('movies/', views.MoviesListApi.as_view(), name='movies-list'),
    path('movies/<int:page>/', views.MoviesListApi.as_view(), name='movies-list-paginated'),
]
