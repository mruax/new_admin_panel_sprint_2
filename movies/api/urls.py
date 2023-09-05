from django.urls import path, include

urlpatterns = [
    path('v1/', include('movies.api.v1.urls')),
    # TODO: по курсу не очень ясно зачем делать версионирование, когда функционал реализован в первой версии
    # path('v2/', include('movies.api.v2.urls')),
]
