from django.urls import path, include

urlpatterns = [
    path('v1/', include('movies.api.v1.urls')),
    # также позже попробую рассмотреть вариант с drf-yasg
    # path('v2/', include('movies.api.v2.urls')),
]
