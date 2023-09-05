from django.urls import path

from movies.api.v1 import views

urlpatterns = [
    path('movies/', views.MoviesListApi.as_view(), name='movies-paginated-list'),  # has a page params through /?page=*
    path('movies/<uuid:pk>/', views.MoviesDetailApi.as_view(), name='movies-filmwork-details'),
]
